from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)


faqs = [
    # Company & Program Overview (1-20)
    {"q": "What is CodeAlpha?", "a": "CodeAlpha is a leading software development company dedicated to driving innovation and excellence across emerging technologies."},
    {"q": "What does the AI internship provide?", "a": "The internship offers hands-on experience in AI model development, machine learning workflows, and real-time data processing."},
    {"q": "CodeAlpha vision and mission", "a": "Our focus is on driving innovation across emerging technologies through dynamic project contributions."},
    {"q": "Who is eligible for this internship?", "a": "Students and candidates looking for real-world experience in AI model building and advanced tech."},
    {"q": "What is the environment like?", "a": "Interns work in a dynamic environment, receiving expert mentorship and contributing to latest AI advancements."},
    {"q": "CodeAlpha website URL", "a": "The official website is www.codealpha.tech."},
    {"q": "is mentorship expert", "a": "Yes, expert mentorship is provided throughout the internship program."},
    {"q": "advanced tech exposure provided", "a": "Interns receive exposure to real-time data processing and model development workflows."},
    {"q": "is the program paid", "a": "The internship is focused on providing real-world project experience and certification perks."},
    {"q": "what is machine learning workflows", "a": "The internship covers training on complete machine learning workflows from data to deployment."},

    # Support & Official Contacts (21-40)
    {"q": "how to contact support", "a": "Reach official support at services@codealpha.tech or WhatsApp at +91 8052293611."},
    {"q": "official email for help", "a": "The official help email is services@codealpha.tech."},
    {"q": "WhatsApp support contact number", "a": "The official WhatsApp support number is +91 8052293611."},
    {"q": "where to report technical issues", "a": "Contact support via the official WhatsApp group or email services@codealpha.tech."},
    {"q": "urgent queries contact", "a": "For urgent matters, use the provided WhatsApp number: +91 8052293611."},
    {"q": "where is the office website", "a": "Official details and contact information are on www.codealpha.tech."},
    {"q": "submission form error support", "a": "Email support if you face issues with the submission form or link."},
    {"q": "general questions channel", "a": "Post general questions in the internship WhatsApp group."},
    {"q": "document verification support", "a": "Contact support via services@codealpha.tech for certificate or official document verification issues."},
    {"q": "contact for LOR status", "a": "Email services@codealpha.tech regarding the status of your Letter of Recommendation."},

    # Eligibility & Rules (41-65)
    {"q": "how many tasks required for certificate", "a": "You must complete a **minimum of two or three projects** from your assigned domain list to be eligible for certification."},
    {"q": "minimum projects for completion", "a": "Eligibility requires successfully finishing at least 2 or 3 tasks within the timeframe."},
    {"q": "is only one task submission okay", "a": "No, submitting only one project will result in an **incomplete status**; certificates will not be issued."},
    {"q": "GitHub naming criteria", "a": "Your repository must be named exactly: **CodeAlpha_ProjectName**."},
    {"q": "mandatory LinkedIn post rules", "a": "Posting a video explanation and sharing your status **tagging @CodeAlpha** is mandatory on LinkedIn."},
    {"q": "LinkedIn tagging rules", "a": "You must tag **@CodeAlpha** in your project status and video explanation posts."},
    {"q": "is public repo mandatory", "a": "Yes, ensure your **GitHub repository is public** for proper evaluation by the team."},
    {"q": "timeframe for projects completion", "a": "Complete tasks within the **mentioned time frame** shared in your instructions."},
    {"q": "video explanation length requirements", "a": "The video should clearly explain your working project model and features."},
    {"q": "certificate non-issuance rules", "a": "Certificates are only issued after **successful submission of 2-3 tasks** and fulfillment of all LinkedIn criteria."},

    # Perks & Rewards (66-90)
    {"q": "internship perks general", "a": "Perks include an **Offer Letter, QR Verified Certificate, LOR, and job opportunities/placement support**."},
    {"q": "what is unique id certificate", "a": "Completion certificates include a unique certificate ID and are QR Verified for authenticity."},
    {"q": "Letter of Recommendation criteria", "a": "A performance-based **LOR is issued to successful participants** after project review."},
    {"q": "job placement opportunities", "a": "CodeAlpha provides **job opportunities and placement support** based on high performance."},
    {"q": "resume building help details", "a": "Resume building support is provided to assist successful candidates in career advancement."},
    {"q": "verify certificate authenticity", "a": "Certificates are authenticated via **QR code and unique ID**."},
    {"q": "is offer letter provided", "a": "Yes, an **Internship Offer Letter** is issued to all participating students at the start of the program."},
    {"q": "mentorship rewards", "a": "Access to expert mentorship is a key perk of the dynamic work environment."},
    {"q": "benefits completing all tasks", "a": "Full eligibility for all program perks, including LOR and placement support."},
    {"q": "career advancement support", "a": "Career and placement support is provided post-task completion for successful candidates."},

    # Submission Process (91-110)
    {"q": "How to submit completed tasks?", "a": "Tasks must be submitted **only through the official Submission Form** shared in your WhatsApp group."},
    {"q": "Where to find submission form link?", "a": "The submission form link is shared directly in your respective **internship WhatsApp group**."},
    {"q": "Can I submit code via email?", "a": "No, all task submissions must go through the **official form link** only."},
    {"q": "Submission detail form source?", "a": "The official link is from the support team in the WhatsApp group."},
    {"q": "following form instructions", "a": "Carefully follow the form's instructions to ensure your submission is accepted and verified."},

    #  Task 1: Language Translation Tool (111-135)
    {"q": "what is Task 1", "a": "Task 1 involves creating a **Language Translation Tool**."},
    {"q": "Task 1 requirement UI", "a": "Create a user interface where users can enter text and select source/target languages."},
    {"q": "API for Task 1", "a": "The tool must integrate an **API** like Google or Microsoft Translator for text translation."},
    {"q": "translation response format display", "a": "Display the clear translated response on the UI screen."},
    {"q": "optional features Task 1", "a": "Optional features include adding speech-to-text or a copy button for better usability."},
    {"q": "UI creation tools Task 1", "a": "Use standard web technologies (HTML/CSS/JS) or any framework to create the user interface."},
    {"q": "source language to target language tool", "a": "The tool should accurately map and translate text between chosen languages."},
    {"q": "is API key needed for task 1", "a": "You will need to set up and use a valid translation API key."},
    {"q": "Task 1 objective", "a": "The objective is to demonstrate skill in API integration and UI development."},

    # --- Task 2: Chatbot for FAQs (136-160) ---
    {"q": "what is  Task 2", "a": "Task 2 is creating a **Chatbot for FAQs** using advanced NLP techniques."},
    {"q": "NLP preprocessing tools for chatbot", "a": "Use NLP libraries like **NLTK or SpaCy** for cleaning, tokenization, and stemming."},
    {"q": "intent matching chatbot algorithm", "a": "Implement **Cosine Similarity** or other intent matching algorithms to find the best response."},
    {"q": "chatbot UI requirements", "a": "Create a simple chat UI for user interaction and displaying bot responses."},
    {"q": "how to match user questions", "a": "Match user questions with the pre-defined FAQ dataset using vector similarity."},
    {"q": "TFIDF vectorization for chatbot", "a": "Use TF-IDF (Term Frequency-Inverse Document Frequency) vectorization for text processing."},
    {"q": "tokenization in chatbot purpose", "a": "Tokenization cleans and prepares user queries for accurate similarity matching."},
    {"q": "Task 2 objective", "a": "The objective is to demonstrate skill in Python backend development and NLP intent recognition."},

    #  Task 3: Music Generation with AI (161-185)
    {"q": "what is  Task 3", "a": "Task 3 involves **Music Generation with AI**."},
    {"q": "Task 3 model type", "a": "Build a deep learning model using **RNNs (like LSTM) or GANs** to learn music patterns."},
    {"q": "dataset for Task 3", "a": "Collect **MIDI music data** (e.g., classical, jazz) to train your AI model."},
    {"q": "music data preprocessing", "a": "Preprocess the data into **note sequences** suitable for training (e.g., using 'music21')."},
    {"q": "music21 library use", "a": "Use the 'music21' library for efficient note sequence processing."},
    {"q": "Task 3 output format", "a": "Convert generated sequences back to **MIDI** and play or save them as audio."},
    {"q": "LSTM model music generation", "a": "Long Short-Term Memory (LSTM) is a recommended RNN structure for sequential data like music."},
    {"q": "Task 3 objective", "a": "The objective is to demonstrate skill in sequential deep learning models and data handling."},

    # --- Task 4: Object Detection and Tracking (186-210) ---
    {"q": "what is  Task 4", "a": "Task 4 is **Object Detection and Tracking**."},
    {"q": "video input setup Task 4", "a": "Set up **real-time video input** using a webcam or video file (OpenCV)."},
    {"q": "detection model Task 4", "a": "Use a pre-trained model like **YOLO or Faster R-CNN** for object detection."},
    {"q": "bounding boxes processing", "a": "Process each video frame to detect objects and **draw bounding boxes**."},
    {"q": "tracking algorithm Task 4", "a": "Apply object tracking using algorithms like **SORT or Deep SORT**."},
    {"q": "Task 4 output display", "a": "Display the output with labels and tracking IDs in real time."},
    {"q": "OpenCV use Task 4", "a": "OpenCV is required for video input setup and frame processing."},
    {"q": "real time processing tools", "a": "OpenCV and detection models are used for real-time video processing."},
    {"q": "Task 4 objective", "a": "The objective is to demonstrate skill in computer vision, real-time processing, and tracking algorithms."}
]

questions = [faq['q'] for faq in faqs]
vectorizer = TfidfVectorizer(stop_words='english')
question_vectors = vectorizer.fit_transform(questions)

@app.route('/ask', methods=['POST'])
def ask():
    user_msg = request.json.get('msg', '').lower().strip()
    
    
    if 'task 1' in user_msg or 'translation tool' in user_msg:
        
        return jsonify({"answer": "TASK 1: Language Translation Tool. Create a UI and integrate an API (like Google Translate) to translate text between languages. Objective: API integration and UI development."})
    
    if 'task 2' in user_msg or 'chatbot instructions' in user_msg:

        return jsonify({"answer": "TASK 2: Chatbot for FAQs. Use NLP techniques (NLTK/SpaCy) for tokenization and implement Cosine Similarity for robust intent matching from the FAQ dataset."})
        
    if 'task 3' in user_msg or 'music generation' in user_msg:
        
        return jsonify({"answer": "TASK 3: Music Generation with AI. Build a deep learning model (RNN/LSTM) and train it on MIDI data (e.g., music21) to generate new music sequences."})

    if 'task 4' in user_msg or 'object detection' in user_msg:
        
        return jsonify({"answer": "TASK 4: Object Detection and Tracking. Use OpenCV and models like YOLO/Faster R-CNN for real-time video detection and tracking (using SORT/Deep SORT algorithms)."})
    
    user_vec = vectorizer.transform([user_msg])
    similarities = cosine_similarity(user_vec, question_vectors)
    best_match_idx = similarities.argmax()
    
    if similarities[0][best_match_idx] > 0.15:
        response = faqs[best_match_idx]['a']
    else:
        response = "I am the CodeAlpha AI Assistant. I can't find that specific detail. Try asking about: 'Task 1 details', 'Perks', or 'WhatsApp number'."
        
    return jsonify({"answer": response})

if __name__ == '__main__':
    app.run(port=5000)
