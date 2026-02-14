// Simple tab handling
const tabButtons = document.querySelectorAll(".tab-button");
const tabContents = document.querySelectorAll(".tab-content");

tabButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
        const targetId = btn.dataset.tab;

        tabButtons.forEach((b) => b.classList.remove("active"));
        tabContents.forEach((c) => c.classList.remove("active"));

        btn.classList.add("active");
        const target = document.getElementById(targetId);
        if (target) target.classList.add("active");
    });
});

/**
 * Basic markdown-to-HTML for headings and bullet lists.
 * This is intentionally minimal; it supports:
 * - #, ##, ### headings
 * - -, * bullets
 * - numbered lists (1., 2., etc.)
 */
function simpleMarkdownToHtml(markdown) {
    if (!markdown) return "";

    const lines = markdown.split(/\r?\n/);
    const htmlLines = [];

    for (let line of lines) {
        const trimmed = line.trim();

        if (trimmed.startsWith("### ")) {
            htmlLines.push(`<h3>${trimmed.slice(4)}</h3>`);
        } else if (trimmed.startsWith("## ")) {
            htmlLines.push(`<h2>${trimmed.slice(3)}</h2>`);
        } else if (trimmed.startsWith("# ")) {
            htmlLines.push(`<h2>${trimmed.slice(2)}</h2>`);
        } else if (/^\d+\.\s+/.test(trimmed)) {
            htmlLines.push(`<p>${trimmed}</p>`);
        } else if (/^[-*]\s+/.test(trimmed)) {
            htmlLines.push(`<p>• ${trimmed.replace(/^[-*]\s+/, "")}</p>`);
        } else if (trimmed === "") {
            htmlLines.push("<br />");
        } else {
            htmlLines.push(`<p>${trimmed}</p>`);
        }
    }

    return htmlLines.join("\n");
}

async function handleFormSubmit({
    formId,
    url,
    outputId,
    statusPillId,
    buttonSelector,
}) {
    const form = document.getElementById(formId);
    const output = document.getElementById(outputId);
    const statusPill = document.getElementById(statusPillId);
    const submitButton = form.querySelector(buttonSelector);

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const body = new URLSearchParams();
        for (const [key, value] of formData.entries()) {
            body.append(key, value);
        }

        submitButton.disabled = true;
        statusPill.textContent = "Thinking with Groq…";
        statusPill.classList.remove("error");
        statusPill.classList.add("loading");
        output.innerHTML = "<p class=\"placeholder\">Generating with LLaMA 3.3 70B…</p>";

        try {
            const resp = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                },
                body: body.toString(),
            });

            const data = await resp.json();

            if (!data.ok) {
                throw new Error(data.error || "Unknown error");
            }

            const html = simpleMarkdownToHtml(data.content);
            output.innerHTML = html || "<p class=\"placeholder\">Empty response from AI.</p>";
            statusPill.textContent = "Completed";
            statusPill.classList.remove("loading", "error");
        } catch (err) {
            console.error(err);
            output.innerHTML =
                '<p class="placeholder" style="color:#f97373;">' +
                "There was an error talking to Groq. Check your API key and try again." +
                "</p>";
            statusPill.textContent = "Error";
            statusPill.classList.remove("loading");
            statusPill.classList.add("error");
        } finally {
            submitButton.disabled = false;
        }
    });
}

// Update campaign button text based on platform selection
const platformSelect = document.getElementById("platform-select");
const campaignSubmitBtn = document.getElementById("campaign-submit-btn");

if (platformSelect && campaignSubmitBtn) {
    platformSelect.addEventListener("change", () => {
        const platform = platformSelect.value;
        campaignSubmitBtn.textContent = `Generate ${platform} Campaign`;
    });
}

handleFormSubmit({
    formId: "campaign-form",
    url: "/api/campaign",
    outputId: "campaign-output",
    statusPillId: "campaign-status-pill",
    buttonSelector: ".primary-btn",
});

handleFormSubmit({
    formId: "pitch-form",
    url: "/api/pitch",
    outputId: "pitch-output",
    statusPillId: "pitch-status-pill",
    buttonSelector: ".primary-btn",
});

handleFormSubmit({
    formId: "lead-form",
    url: "/api/lead-score",
    outputId: "lead-output",
    statusPillId: "lead-status-pill",
    buttonSelector: ".primary-btn",
});

