# MarketAI Suite - Test Cases Documentation

This document provides step-by-step instructions for testing all three core features of MarketAI Suite.

---

## Prerequisites

1. **Flask app is running**: `python app.py`
2. **Browser open**: Navigate to `http://127.0.0.1:5000`
3. **Groq API key configured**: Ensure `.env` file contains your `GROQ_API_KEY`

---

## Test Case 1: Marketing Campaign Generation

### Objective
Test the AI-powered marketing campaign generator for multiple platforms.

### Steps

1. **Navigate to Campaign Generator**
   - Click on the **"Marketing Campaign"** tab (should be active by default)

2. **Fill in the form fields:**
   - **Product name**: `AI-powered email marketing platform`
   - **Product description**: `An intelligent email marketing platform that uses AI to optimize send times, personalize content, and increase open rates for e-commerce businesses.`
   - **Target audience**: `Marketing managers, mid-size e-commerce companies, budget-conscious`
   - **Platform**: Select from dropdown:
     - First test: Select **"LinkedIn"**
     - Second test: Select **"Instagram"** (run separately for multi-platform testing)
   - **Campaign objective**: `Generate qualified leads and demo bookings`
   - **Tone & style**: `Professional, data-driven, ROI-focused`

3. **Click "Generate Marketing Campaign"** (button text will update based on selected platform)

### Expected Results

✅ **Status**: Should show "Thinking with Groq…" then "Completed"

✅ **Output should include**:
- **Campaign Objectives** (2-3 specific, measurable goals)
- **Platform-Specific Strategy** (posting times, formats, best practices)
- **Audience Insight Summary** (behavior on selected platform)
- **5 Targeted Content Ideas** (with formats and hashtags if applicable)
- **3 Variations of Ad Copy** (platform-optimized, respecting character limits)
- **Recommended CTAs** (platform-specific)
- **Content Calendar Suggestions** (posting frequency, best times)
- **Performance Metrics** (KPIs to track)

### Notes
- **Multi-platform testing**: Since the form supports one platform at a time, run the test twice:
  - First with "LinkedIn" selected
  - Then with "Instagram" selected
- Each platform will generate different content formats (LinkedIn = professional posts, Instagram = visual content + hashtags)

---

## Test Case 2: Sales Pitch Generation

### Objective
Test the intelligent sales pitch generator for enterprise B2B scenarios.

### Steps

1. **Navigate to Sales Pitch Generator**
   - Click on the **"Sales Pitch"** tab

2. **Fill in the form fields:**
   - **Solution name**: `Cloud-based inventory management system`
   - **Prospect role**: `Operations Director`
   - **Prospect company**: `Fortune 500 retail company, scaling operations across 500 stores`
   - **Key pain points**: `Manual inventory tracking across 500 stores, stockouts causing lost sales, real-time visibility challenges, scaling operations efficiently`
   - **Desired outcome**: `Secure a technical evaluation meeting and pilot program approval`

3. **Click "Generate enterprise pitch"**

### Expected Results

✅ **Status**: Should show "Thinking with Groq…" then "Completed"

✅ **Output should include**:
- **30-Second Elevator Pitch** (3-5 sentences, conversational)
- **Clear Value Proposition** (3-5 bullet points addressing pain points)
- **Key Differentiators** (3-5 bullets highlighting competitive advantages)
- **Risk & Objection Handling** (2-3 common objections with responses)
- **Strategic Call To Action** (1-2 next steps tailored to Operations Director)

### Notes
- The pitch should be executive-ready and address enterprise-scale challenges
- Content should focus on operational efficiency and scalability

---

## Test Case 3: Lead Scoring & Qualification

### Objective
Test the AI-powered lead qualification and scoring system using BANT/MEDDIC methodology.

### Steps

1. **Navigate to Lead Scoring**
   - Click on the **"Lead Scoring"** tab

2. **Fill in the form fields:**
   - **Lead name** (optional): `Sarah Johnson`
   - **Budget**: `$150,000 annual software budget, can approve deals up to $50,000`
   - **Urgency**: `High - Board of directors requested solution by end of Q3`
   - **Timeline**: `End of Q3 (approximately 3 months)`
   - **Company size**: `Enterprise - 5000+ employees`
   - **Industry**: `E-commerce / Retail`
   - **Decision-maker role**: `VP of Customer Success`
   - **Use case summary**: `Improving customer retention by 20%, reducing churn. Current churn rate is 15% annually, goal is to reduce to 12% or lower. Need solution that integrates with existing CRM and provides predictive analytics.`

3. **Click "Score this lead"**

### Expected Results

✅ **Status**: Should show "Thinking with Groq…" then "Completed"

✅ **Output should include**:
- **Lead Score Summary**
  - Score: X/100 (should be high given budget, urgency, and clear need)
  - Probability of conversion: Y% (should reflect urgency and budget)
- **Qualification Breakdown**
  - **Budget**: Analysis of $150K budget and $50K approval authority
  - **Authority**: VP-level decision maker assessment
  - **Need**: Clear need (20% retention improvement, churn reduction)
  - **Timeline**: Q3 deadline urgency
  - **Fit / Ideal Customer Profile**: Enterprise e-commerce fit
- **Detailed Reasoning** (paragraphs explaining score calculation)
- **Recommended Next Actions** (3-5 concrete follow-up steps)

### Notes
- Given the high budget, urgency, clear need, and VP-level authority, this lead should score **75-90/100**
- The probability of conversion should be **60-80%** given the urgency and clear requirements
- Next actions should prioritize fast-tracking due to Q3 deadline

---

## Test Case 4: Error Handling

### Objective
Test error handling when API key is missing or invalid.

### Steps

1. **Temporarily remove or invalidate API key**
   - Edit `.env` file and change `GROQ_API_KEY` to an invalid value
   - Restart Flask app: `python app.py`

2. **Try any of the three features** (Campaign, Pitch, or Lead Scoring)

### Expected Results

✅ **Status**: Should show "Error" badge

✅ **Output**: Should display error message:
   - `"There was an error talking to Groq. Check your API key and try again."`

### Notes
- Restore valid API key after testing
- Error should be user-friendly and not expose technical details

---

## Test Case 5: Platform-Specific Content Validation

### Objective
Verify that different platforms generate appropriately formatted content.

### Steps

1. **Test LinkedIn Campaign**
   - Select "LinkedIn" platform
   - Generate campaign
   - Verify: Content should be professional, B2B-focused, no hashtags overuse

2. **Test Instagram Campaign**
   - Select "Instagram" platform
   - Generate campaign
   - Verify: Content should include hashtag suggestions, visual content ideas, Stories/Reels recommendations

3. **Test Twitter/X Campaign**
   - Select "Twitter/X" platform
   - Generate campaign
   - Verify: Content should be concise (280 chars), thread suggestions if needed

4. **Test Email Marketing Campaign**
   - Select "Email Marketing" platform
   - Generate campaign
   - Verify: Should include subject lines (50-60 chars), email copy structure

### Expected Results

✅ Each platform should generate content that:
- Respects platform character limits
- Uses appropriate content formats
- Includes platform-specific best practices
- Provides relevant CTAs for that platform

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'dotenv'"
**Solution**: Run `pip install -r requirements.txt`

### Issue: "Error talking to Groq"
**Solution**: 
1. Check `.env` file has valid `GROQ_API_KEY`
2. Verify API key is active at https://console.groq.com
3. Check internet connectivity

### Issue: Form submission does nothing
**Solution**:
1. Check browser console for JavaScript errors (F12)
2. Verify Flask app is running
3. Check network tab for API call status

### Issue: Output is empty or malformed
**Solution**:
1. Check Flask terminal for error messages
2. Verify Groq API response in browser Network tab
3. Check that API key has sufficient credits/quota

---

## Success Criteria

All test cases pass if:
- ✅ Forms submit successfully
- ✅ AI generates comprehensive, structured output
- ✅ Content is platform-appropriate (for campaigns)
- ✅ Lead scores are reasonable and well-reasoned
- ✅ Error handling works gracefully
- ✅ UI updates correctly (loading states, status badges)

---

## Additional Notes

- **Response Time**: Groq API typically responds in 2-5 seconds
- **Content Quality**: AI output may vary slightly between runs (temperature=0.4 for consistency)
- **Platform Support**: Currently supports 10 platforms (LinkedIn, Facebook, Instagram, Twitter/X, Email, YouTube, TikTok, Google Ads, Pinterest, Snapchat)
- **Multi-platform**: To generate campaigns for multiple platforms, run the generator separately for each platform

---

**Last Updated**: February 13, 2026
**Version**: 1.0
