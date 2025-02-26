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
1. **Select Language** 🌐
2. **Input YouTube URL** 🎬
3. **View Generated Recipe** ✨
4. **Copy or Save Recipe** 📚
5. **Provide Feedback** 📝

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
