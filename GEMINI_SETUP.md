# 🔑 Setting Up Your Gemini API Key

Follow these steps to connect AEGIS to Google's Gemini AI:

## Step 1: Get Your API Key

1. **Go to Google AI Studio**: https://aistudio.google.com/app/apikey
2. **Sign in** with your Google account
3. Click **"Get API Key"** or **"Create API Key"**
4. **Copy the key** (it starts with `AIza...`)

> ⚠️ **Keep your API key secret!** Never share it or commit it to version control.

---

## Step 2: Create .env File

1. **Navigate to your project folder**:
   ```
   C:\Users\RAJ SINGH\OneDrive\Desktop\geminihackethon
   ```

2. **Create a new file** named `.env` (note the dot at the start)

3. **Add your API key**:
   ```env
   GEMINI_API_KEY=AIza...your_actual_key_here
   GEMINI_MODEL=gemini-2.0-flash-exp
   ```

4. **Save the file**

### Example .env file:
```env
# Google Gemini API
GEMINI_API_KEY=AIzaSyC1234567890abcdefghijklmnopqrstuvw
GEMINI_MODEL=gemini-2.0-flash-exp

# Django Settings (already configured)
DEBUG=True
SECRET_KEY=django-insecure-bjf#!8=3hnua7jz&y0!$vmn#r*i%ib@x$q1g5kli%6&eys!kt7
```

---

## Step 3: Restart the Server

1. **Stop the current server** (press `Ctrl+C` in the terminal)

2. **Restart it**:
   ```bash
   python manage.py runserver
   ```

3. **Look for this message**:
   ```
   Gemini client initialized with model: gemini-2.0-flash-exp
   AuditorOrchestrator initialized with Gemini AI
   ```

   ✅ If you see this, Gemini is connected!
   
   ⚠️ If you see "Simulation mode", check your API key.

---

## Step 4: Test It!

1. **Open the dashboard**: http://localhost:8000

2. **Send a test message**:
   ```
   analyze safety protocols for surgical procedures
   ```

3. **You should see**:
   - Real AI-generated response (not simulated!)
   - More intelligent, context-aware answers
   - Proper function calling when needed

---

## Troubleshooting

### Problem: "Simulation mode" message

**Cause**: API key not found or invalid

**Solution**:
1. Check that `.env` file exists in project root
2. Verify `GEMINI_API_KEY=` has your actual key
3. Make sure there are no spaces around the `=`
4. Restart the server

### Problem: "API key not valid"

**Cause**: Invalid or expired API key

**Solution**:
1. Go back to Google AI Studio
2. Create a new API key
3. Update your `.env` file
4. Restart the server

### Problem: "Rate limit exceeded"

**Cause**: Too many requests to Gemini API

**Solution**:
1. Wait a few minutes
2. Consider upgrading your API quota
3. Use `gemini-1.5-flash` for faster, cheaper requests

---

## Model Options

You can change the model in your `.env` file:

### Recommended Models:

**gemini-2.0-flash-exp** (Default)
- ✅ Fastest responses
- ✅ Supports function calling
- ✅ Multimodal (text, images, video)
- ✅ Free tier available

**gemini-1.5-pro-latest**
- ✅ 2M token context window
- ✅ Best for knowledge grounding
- ✅ Most capable reasoning
- ⚠️ Slower, more expensive

**gemini-1.5-flash**
- ✅ Balanced speed/capability
- ✅ Good for most use cases
- ✅ Lower cost

---

## What Changes After Integration?

### Before (Simulation):
- Keyword-based responses
- Simple pattern matching
- Limited understanding

### After (Real Gemini):
- **Intelligent analysis** of your inputs
- **Context-aware** responses
- **Proactive tool calling** when it detects issues
- **Natural conversation** flow
- **Deep understanding** of safety protocols

---

## Example Interactions

### Test 1: Safety Violation
**You**: `"I see someone without gloves touching the sterile field"`

**Gemini will**:
1. Analyze the severity
2. Call `log_deviation` tool automatically
3. Provide detailed recommendations
4. Save to database

### Test 2: Protocol Query
**You**: `"What are the requirements for anesthesia monitoring?"`

**Gemini will**:
1. Call `search_knowledge_vault` tool
2. Retrieve relevant protocols
3. Explain the requirements clearly

### Test 3: General Monitoring
**You**: `"Begin monitoring operating room 3"`

**Gemini will**:
1. Acknowledge the request
2. Explain what it's watching for
3. Maintain context for follow-up questions

---

## Security Best Practices

✅ **DO**:
- Keep `.env` file in `.gitignore`
- Use environment variables for sensitive data
- Rotate API keys periodically
- Monitor API usage

❌ **DON'T**:
- Commit `.env` to Git
- Share your API key
- Hardcode keys in source code
- Use production keys in development

---

## Next Steps

Once Gemini is connected:

1. **Test thoroughly** with various inputs
2. **Monitor API usage** in Google AI Studio
3. **Customize the system instruction** in `gemini_client.py`
4. **Add more tools** for specific use cases
5. **Implement context caching** for knowledge vault

---

**Need help?** Check the server logs for detailed error messages:
```bash
# The terminal where you ran: python manage.py runserver
```

---

*You're now running AEGIS with real AI! 🚀*
