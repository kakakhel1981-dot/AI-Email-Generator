import os
import streamlit as st

# ============================================================
# AI EMAIL GENERATOR v3.6
# Developed by Shahzad Amin
# ============================================================

# Import Google Gen AI SDK
try:
    from google import genai
except ImportError as e:
    st.error("❌ Google Gen AI SDK could not be imported.")
    st.error(
        "Please make sure google-genai is installed "
        "through requirements.txt."
    )
    st.code(str(e))
    st.stop()


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Email Generator v3.6",
    page_icon="✉️",
    layout="centered"
)


# ============================================================
# HEADER
# ============================================================

st.title("✉️ AI Email Generator")

st.subheader(
    "Generate professional emails with AI"
)

st.write(
    "Enter the email details below and Gemini will generate "
    "a complete, professional, ready-to-use email."
)


# ============================================================
# GEMINI API KEY
# ============================================================

try:

    API_KEY = st.secrets["GEMINI_API_KEY"]

except Exception:

    API_KEY = os.environ.get("GEMINI_API_KEY")


if not API_KEY:

    st.error(
        "❌ Gemini API key was not found."
    )

    st.info(
        "Please add GEMINI_API_KEY in "
        "Streamlit Cloud → App Settings → Secrets."
    )

    st.stop()


# ============================================================
# GEMINI CLIENT
# ============================================================

try:

    client = genai.Client(
        api_key=API_KEY
    )

except Exception as error:

    st.error("❌ Unable to generate the email.")

    st.error(f"Gemini API Error: {str(error)}")

    with st.expander("🔍 Technical Error Details"):

        st.exception(error)


# ============================================================
# GEMINI MODEL
# ============================================================

PRIMARY_MODEL = "gemini-3.6-flash"


# ============================================================
# EMAIL GENERATION FUNCTION
# ============================================================

def generate_email(
    recipient,
    purpose,
    key_points,
    tone,
    length
):

    # --------------------------------------------------------
    # TONE INSTRUCTIONS
    # --------------------------------------------------------

    tone_instructions = {

        "Professional": """
Use a professional business communication style.

The email should be:
- Clear
- Respectful
- Structured
- Professional
- Appropriate for workplace communication

Avoid unnecessary casual expressions.
""",

        "Formal": """
Use a highly formal and polished business style.

The email should:
- Use formal business language
- Use complete sentences
- Be respectful and precise
- Avoid contractions
- Avoid casual expressions
""",

        "Friendly": """
Use a warm, positive, and approachable tone.

The email should:
- Feel natural and friendly
- Remain professional
- Use positive language
- Maintain a respectful business tone
""",

        "Polite": """
Use a very courteous and respectful tone.

The email should:
- Make requests diplomatically
- Avoid demanding language
- Avoid harsh expressions
- Clearly communicate the request
""",

        "Casual": """
Use a relaxed and natural communication style.

The email should:
- Be easy to read
- Sound friendly
- Avoid unnecessarily formal language
- Remain appropriate for the recipient and purpose
"""
    }


    # --------------------------------------------------------
    # LENGTH INSTRUCTIONS
    # --------------------------------------------------------

    length_instructions = {

        "Short": """
Keep the email concise.

Requirements:
- Approximately 3–6 sentences
- Include only essential information
- Avoid unnecessary explanation
""",

        "Medium": """
Provide a balanced email.

Requirements:
- Approximately 2–4 short paragraphs
- Include sufficient context
- Cover all important points
- Avoid unnecessary detail
""",

        "Detailed": """
Provide a comprehensive and well-structured email.

Requirements:
- Use multiple paragraphs where appropriate
- Address all important key points
- Provide sufficient context
- Maintain clarity
- Do not add information that was not provided
"""
    }


    selected_tone = tone_instructions[tone]

    selected_length = length_instructions[length]


    # --------------------------------------------------------
    # PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are an advanced AI Email Generator.

Create a professional, clear, accurate,
and ready-to-send email.

============================================================
EMAIL INFORMATION
============================================================

Recipient:
{recipient}

Email Purpose:
{purpose}

Key Points:
{key_points}

Selected Tone:
{tone}

Selected Length:
{length}

============================================================
TONE REQUIREMENTS
============================================================

{selected_tone}

============================================================
LENGTH REQUIREMENTS
============================================================

{selected_length}

============================================================
EMAIL GENERATION RULES
============================================================

1. Generate a clear and relevant subject.

2. Write a complete email body.

3. Include an appropriate greeting.

4. Clearly communicate the purpose of the email.

5. Include all important key points.

6. Do not invent facts.

7. Do not invent names.

8. Do not invent dates.

9. Do not invent numbers.

10. Do not invent commitments.

11. Do not invent technical information.

12. Do not change the meaning of the user's information.

13. Maintain the selected tone.

14. Follow the selected length.

15. Use correct grammar and professional English.

16. Use paragraphs where appropriate.

17. Make the email ready to copy and send.

18. Include an appropriate professional closing.

19. Do not explain how the email was generated.

============================================================
OUTPUT FORMAT
============================================================

Subject:
<generated subject>

Email:
<complete email body>
"""


    # --------------------------------------------------------
    # GEMINI REQUEST
    # --------------------------------------------------------

    response = client.models.generate_content(
        model=PRIMARY_MODEL,
        contents=prompt
    )


    if not response.text:

        raise Exception(
            "Gemini returned an empty response."
        )


    return response.text


# ============================================================
# EMAIL INPUTS
# ============================================================

st.markdown("### 📧 Email Details")


recipient = st.text_input(
    "Recipient",
    placeholder="e.g., IT Support Team"
)


purpose = st.text_input(
    "Email Purpose",
    placeholder="e.g., Request technical support"
)


key_points = st.text_area(
    "Key Points",
    placeholder=(
        "Enter the important information you want "
        "to include in the email..."
    ),
    height=150
)


# ============================================================
# EMAIL TONE
# ============================================================

tone = st.selectbox(
    "Email Tone",
    [
        "Professional",
        "Formal",
        "Friendly",
        "Polite",
        "Casual"
    ]
)


# ============================================================
# EMAIL LENGTH
# ============================================================

length = st.selectbox(
    "Email Length",
    [
        "Short",
        "Medium",
        "Detailed"
    ]
)


# ============================================================
# GENERATE EMAIL
# ============================================================

if st.button(
    "✨ Generate Email",
    use_container_width=True
):

    if not recipient.strip():

        st.warning(
            "⚠️ Please enter the recipient."
        )

    elif not purpose.strip():

        st.warning(
            "⚠️ Please enter the email purpose."
        )

    elif not key_points.strip():

        st.warning(
            "⚠️ Please enter the key points."
        )

    else:

        with st.spinner(
            "🤖 Generating your email..."
        ):

            try:

                generated_email = generate_email(
                    recipient=recipient,
                    purpose=purpose,
                    key_points=key_points,
                    tone=tone,
                    length=length
                )


                st.success(
                    "✅ Email generated successfully!"
                )


                st.text_area(
                    "Generated Email",
                    value=generated_email,
                    height=450
                )


                st.info(
                    "💡 Copy the generated email "
                    "from the text box above."
                )


            except Exception as error:

                st.error(
                    "❌ Unable to generate the email."
                )

                st.warning(
                    "Please check your Gemini API key "
                    "and try again."
                )

                with st.expander(
                    "Technical Error Details"
                ):

                    st.code(
                        str(error)
                    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Email Generator v3.6 | Powered by Gemini | "
    "Developed by Shahzad Amin"
)
