# 🍲 YumTube: AI-Powered Recipe Generator 🧠
## Technical Documentation

## 🚀 Executive Summary
YumTube transforms YouTube cooking videos with existing subtitles into structured, easy-to-follow recipes using AI. The application accesses available video captions, processes them through an LLM, and generates well-formatted recipes that can be translated into multiple Indian languages.

## 🏗️ Core Architecture

### 🔄 System Overview
YumTube operates through a seamless integration of AI processing, data storage, and user interface components:

```
[YouTube Video Subtitles] → [Transcript Extraction] → [LLM Processing] → [Recipe Generation] → [User Interface]
                                                                        ↓
                            [User Authentication] ← [Database Storage] ← [Recipe Translation]
```

### 🧩 Key Components

#### 🖥️ Frontend Layer
- **Platform**: Streamlit
- **Function**: User interface for URL input, recipe display, and language selection

#### 🔍 Data Processing Layer
- **Core Engine**: Llama 3.3 70B Versatile (via Groq)
- **Input**: Pre-existing YouTube video subtitles
- **Output**: Structured recipe format

#### 💾 Storage Layer
- **Technology**: Supabase (PostgreSQL-based)
- **Data Models**: User profiles, saved recipes, feedback

#### 🌐 Translation Layer
- **Service**: Sarvam API
- **Supported Languages**: Multiple Indian languages including Hindi, Tamil, Telugu, Kannada, Malayalam, Gujarati, Marathi, Bengali, Punjabi, Oriya, Assamese, etc

## ✨ Feature Suite

### 1. 🧠 Intelligent Recipe Generation
- Accesses existing subtitles from YouTube cooking videos using `youtube-transcript-api`
- Processes caption content through Llama 3.3 70B Versatile via Groq
- Structures unorganized video dialogue into formatted recipe components:
  - Recipe title and description
  - Ingredients with measurements
  - Step-by-step cooking instructions
  - Flavour, texture profile and serving information

### 2. 🗣️ Multilingual Support
- Delivers recipes in multiple Indian languages including Hindi, Tamil, Telugu, Kannada, Malayalam, Gujarati, Marathi, Bengali, Punjabi, Oriya, and Assamese
- Maintains formatting integrity across translations
- Allows users to switch between languages seamlessly

### 3. 📚 User Recipe Management
- **Recipe Saving** 💾
  - Personal recipe library for authenticated users
  - Organized storage with video reference links
  - Language preference retention

- **Recipe Sharing** 📤
  - One-click copy functionality
  - Formatted output for easy sharing

### 4. 👤 User Experience
- **Authentication System** 🔐
  - Streamlined Google login integration
  - Secure session management
  - Profile-based recipe storage

- **Feedback Collection** 📝
  - In-app feedback submission via Streamlit interface
  - Feedback stored in Supabase database
  - Simple form-based input for user comments

## 🛠️ Technology Ecosystem

### 🔧 Core Technologies
| Component | Technology | Purpose |
|-----------|------------|---------|
| 🖥️ Application Framework | Streamlit | End-to-end application delivery |
| 🧠 Language Model | Llama 3.3 70B Versatile | Natural language understanding |
| ⚡ Inference Platform | Groq | High-performance LLM processing |
| 💾 Database | Supabase | User data and recipe storage |
| 🌐 Translation | Sarvam API | Multilingual recipe conversion |
| 🎬 Video Integration | youtube-transcript-api | Subtitle extraction |
| 🔐 Authentication | Supabase Auth + Google OAuth | User identity management |
| ☁️ Deployment | Streamlit Cloud | Application hosting |

### 🤔 Architectural Decisions

#### Why Streamlit? 🖥️
Streamlit was selected for its ability to rapidly develop data-driven applications with minimal frontend expertise required. It enables quick iteration on features while providing a responsive user interface that works well for text-heavy recipe content.

#### Why Groq? ⚡
Groq's inference platform was selected for its exceptional performance in serving large language models like Llama 3.3 70B. Groq's hardware architecture is specifically designed for LLM inference, providing significantly faster response times compared to traditional GPU-based solutions. This speed advantage is crucial for YumTube's user experience, ensuring that recipe generation happens within seconds rather than minutes. Additionally, Groq's optimized API integration simplifies the development process while maintaining high throughput and low latency, which is essential when processing potentially lengthy cooking video transcripts.

#### Why Llama 3.3 70B? 🧠
This LLM was chosen for its exceptional understanding of context and instruction following, which is crucial for accurately interpreting cooking videos and structuring recipes in a natural, human-readable format.

#### Why Supabase? 💾
Supabase provides a comprehensive backend solution that combines authentication, database, and real-time capabilities. This reduces integration complexity and allows for faster development cycles.

#### Why Sarvam API? 🌐
Sarvam excels specifically at Indian language translations, providing more culturally accurate translations of culinary terms compared to general-purpose translation APIs. It supports a comprehensive range of Indian languages, making recipes accessible to a diverse linguistic audience across India.

## 👨‍🍳 User Experience Flow
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600">
  <!-- Background -->
  <rect width="800" height="600" fill="#f9f9f9"/>
  
  <!-- Nodes -->
  <!-- Start -->
  <circle cx="400" cy="40" r="25" fill="#4CAF50" stroke="#388E3C" stroke-width="2"/>
  <text x="400" y="45" font-family="Arial" font-size="14" fill="white" text-anchor="middle">Start</text>
  
  <!-- Visit App -->
  <rect x="330" y="80" width="140" height="40" rx="5" fill="#E3F2FD" stroke="#1976D2" stroke-width="2"/>
  <text x="400" y="105" font-family="Arial" font-size="14" fill="#333" text-anchor="middle">User Visits YumTube</text>
  
  <!-- Select Language -->
  <rect x="330" y="140" width="140" height="40" rx="5" fill="#E3F2FD" stroke="#1976D2" stroke-width="2"/>
  <text x="400" y="165" font-family="Arial" font-size="14" fill="#333" text-anchor="middle">Select Language</text>
  
  <!-- Input URL -->
  <rect x="330" y="200" width="140" height="40" rx="5" fill="#E3F2FD" stroke="#1976D2" stroke-width="2"/>
  <text x="400" y="225" font-family="Arial" font-size="14" fill="#333" text-anchor="middle">Input YouTube URL</text>
  
  <!-- Has Subtitles? -->
  <polygon points="400,260 450,290 400,320 350,290" fill="#FFF9C4" stroke="#FFC107" stroke-width="2"/>
  <text x="400" y="295" font-family="Arial" font-size="14" fill="#333" text-anchor="middle">Has Subtitles?</text>
  
  <!-- Fetch Subtitles -->
  <rect x="470" y="270" width="140" height="40" rx="5" fill="#E3F2FD" stroke="#1976D2" stroke-width="2"/>
  <text x="540" y="295" font-family="Arial" font-size="14" fill="#333" text-anchor="middle">Fetch Subtitles</text>
  
  <!-- Error Message -->
  <rect x="190" y="270" width="140" height="40" rx="5" fill="#FFEBEE" stroke="#F44336" stroke-width="2"/>
  <text x="260" y="295" font-family="Arial" font-size="14" fill="#333" text-anchor="middle">Error Message</text>
  
  <!-- Process Subtitles -->
  <rect x="470" y="330" width="140" height="40" rx="5" fill="#2196F3" stroke="#1565C0" stroke-width="2"/>
  <text x="540" y="355" font-family="Arial" font-size="14" fill="white" text-anchor="middle">Process with LLM</text>
  
  <!-- Generate Recipe -->
  <rect x="470" y="390" width="140" height="40" rx="5" fill="#2196F3" stroke="#1565C0" stroke-width="2"/>
  <text x="540" y="415" font-family="Arial" font-size="14" fill="white" text-anchor="middle">Generate Recipe</text>
  
  <!-- Display Recipe -->
  <rect x="330" y="390" width="140" height="40" rx="5" fill="#2196F3" stroke="#1565C0" stroke-width="2"/>
  <text x="400" y="415" font-family="Arial" font-size="14" fill="white" text-anchor="middle">Display Recipe</text>
  
  <!-- User Action -->
  <polygon points="400,450 450,480 400,510 350,480" fill="#FFF9C4" stroke="#FFC107" stroke-width="2"/>
  <text x="400" y="485" font-family="Arial" font-size="14" fill="#333" text-anchor="middle">User Action?</text>
  
  <!-- Copy -->
  <rect x="190" y="460" width="140" height="40" rx="5" fill="#E3F2FD" stroke="#1976D2" stroke-width="2"/>
  <text x="260" y="485" font-family="Arial" font-size="14" fill="#333" text-anchor="middle">Copy to Clipboard</text>
  
  <!-- Save -->
  <rect x="610" y="460" width="140" height="40" rx="5" fill="#E3F2FD" stroke="#1976D2" stroke-width="2"/>
  <text x="680" y="485" font-family="Arial" font-size="14" fill="#333" text-anchor="middle">Save Recipe</text>
  
  <!-- End/Continue -->
  <rect x="330" y="530" width="140" height="40" rx="5" fill="#E3F2FD" stroke="#1976D2" stroke-width="2"/>
  <text x="400" y="555" font-family="Arial" font-size="14" fill="#333" text-anchor="middle">Continue or End</text>
  
  <!-- End -->
  <circle cx="400" cy="600" r="25" fill="#F44336" stroke="#D32F2F" stroke-width="2"/>
  <text x="400" y="605" font-family="Arial" font-size="14" fill="white" text-anchor="middle">End</text>
  
  <!-- Connections -->
  <!-- Main flow -->
  <line x1="400" y1="65" x2="400" y2="80" stroke="#333" stroke-width="2"/>
  <line x1="400" y1="120" x2="400" y2="140" stroke="#333" stroke-width="2"/>
  <line x1="400" y1="180" x2="400" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="400" y1="240" x2="400" y2="260" stroke="#333" stroke-width="2"/>
  
  <!-- Has Subtitles branch -->
  <line x1="450" y1="290" x2="470" y2="290" stroke="#333" stroke-width="2"/>
  <polygon points="465,285 470,290 465,295" fill="#333"/>
  
  <line x1="350" y1="290" x2="330" y2="290" stroke="#333" stroke-width="2"/>
  <polygon points="335,285 330,290 335,295" fill="#333"/>
  
  <line x1="330" y1="290" x2="310" y2="290" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  
  <!-- Process flow -->
  <line x1="540" y1="310" x2="540" y2="330" stroke="#333" stroke-width="2"/>
  <polygon points="535,325 540,330 545,325" fill="#333"/>
  
  <line x1="540" y1="370" x2="540" y2="390" stroke="#333" stroke-width="2"/>
  <polygon points="535,385 540,390 545,385" fill="#333"/>
  
  <line x1="470" y1="410" x2="450" y2="410" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  
  <!-- Display to Action -->
  <line x1="400" y1="430" x2="400" y2="450" stroke="#333" stroke-width="2"/>
  <polygon points="395,445 400,450 405,445" fill="#333"/>
  
  <!-- Action branches -->
  <line x1="350" y1="480" x2="330" y2="480" stroke="#333" stroke-width="2"/>
  <polygon points="335,475 330,480 335,485" fill="#333"/>
  
  <line x1="450" y1="480" x2="610" y2="480" stroke="#333" stroke-width="2"/>
  <polygon points="605,475 610,480 605,485" fill="#333"/>
  
  <!-- To continue -->
  <line x1="260" y1="500" x2="260" y2="550" stroke="#333" stroke-width="2"/>
  <line x1="260" y1="550" x2="330" y2="550" stroke="#333" stroke-width="2"/>
  <polygon points="325,545 330,550 325,555" fill="#333"/>
  
  <line x1="680" y1="500" x2="680" y2="550" stroke="#333" stroke-width="2"/>
  <line x1="680" y1="550" x2="470" y2="550" stroke="#333" stroke-width="2"/>
  <polygon points="475,545 470,550 475,555" fill="#333"/>
  
  <!-- End connection -->
  <line x1="400" y1="570" x2="400" y2="575" stroke="#333" stroke-width="2"/>
  <polygon points="395,570 400,575 405,570" fill="#333"/>
  
  <!-- Error to URL -->
  <line x1="260" y1="310" x2="260" y2="220" stroke="#333" stroke-width="2"/>
  <line x1="260" y1="220" x2="330" y2="220" stroke="#333" stroke-width="2"/>
  <polygon points="325,215 330,220 325,225" fill="#333"/>
  
  <!-- Definitions -->
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="0" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
  
  <!-- Legend -->
  <rect x="620" y="40" width="20" height="20" fill="#4CAF50" stroke="#388E3C" stroke-width="1"/>
  <text x="650" y="55" font-family="Arial" font-size="12" fill="#333">Start/End Points</text>
  
  <rect x="620" y="70" width="20" height="20" fill="#FFF9C4" stroke="#FFC107" stroke-width="1"/>
  <text x="650" y="85" font-family="Arial" font-size="12" fill="#333">Decision Points</text>
  
  <rect x="620" y="100" width="20" height="20" fill="#2196F3" stroke="#1565C0" stroke-width="1"/>
  <text x="650" y="115" font-family="Arial" font-size="12" fill="#333">Processing Steps</text>
  
  <rect x="620" y="130" width="20" height="20" fill="#E3F2FD" stroke="#1976D2" stroke-width="1"/>
  <text x="650" y="145" font-family="Arial" font-size="12" fill="#333">User Interface</text>
  
  <rect x="620" y="160" width="20" height="20" fill="#FFEBEE" stroke="#F44336" stroke-width="1"/>
  <text x="650" y="175" font-family="Arial" font-size="12" fill="#333">Errors</text>
  
  <!-- Title -->
  <text x="400" y="20" font-family="Arial" font-size="18" font-weight="bold" fill="#333" text-anchor="middle">YumTube User Flow Diagram</text>
</svg>

## 🚀 Deployment Strategy

### ☁️ Hosting Environment
YumTube is deployed on Streamlit Cloud, providing:
- Scalable hosting infrastructure
- Secure environment variable management
- Continuous deployment from GitHub repository

## 🔒 Security Framework

### 🛡️ Data Protection
- API keys managed via secure environment variables
- User authentication handled through established OAuth providers
- No storage of sensitive YouTube account information

## ⚠️ Technical Limitations

- Only works with videos that already have subtitles/captions
- No capability to generate captions for videos without them
- Translation accuracy varies with culinary terminology complexity

## 🔮 Future Roadmap

### 🔜 Planned Enhancements
- 🤖 RAG (Retrieval-Augmented Generation) implementation for chat with recipes functionality
- 🎤 Audio-to-text conversion via ASR when video transcripts are unavailable

## 🎯 Conclusion
YumTube represents a practical application of AI to solve everyday cooking challenges. By bridging video content with structured recipes and adding multilingual support, it creates value for cooking enthusiasts across language barriers. The architecture prioritizes user experience while leveraging cutting-edge language models to deliver high-quality recipe extraction.

---

*Bon Appétit! From YouTube to Your Kitchen* 🍳👨‍🍳👩‍🍳
