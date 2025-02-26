# YumTube: AI-Powered Recipe Generator
## Technical Documentation

## Executive Summary
YumTube transforms YouTube cooking video subtitles into structured, easy-to-follow recipes using AI. By leveraging advanced language models and intelligent transcript processing, the platform helps cooking enthusiasts convert video subtitles into practical text recipes that can be saved, translated, and shared across multiple Indian languages.

## Core Architecture
**Note:** YumTube processes YouTube video subtitles/transcripts only - it does not perform video-to-text conversion or analyze video content directly.

### System Overview
YumTube operates through a seamless integration of AI processing, data storage, and user interface components:

```
[YouTube Video Subtitles] → [Transcript Extraction] → [LLM Processing] → [Recipe Generation] → [User Interface]
                                                                        ↓
                            [User Authentication] ← [Database Storage] ← [Recipe Translation]
```

### Key Components

#### Frontend Layer
- **Platform**: Streamlit
- **Function**: Provides an intuitive web interface for URL input, recipe display, language selection, and user account management
- **Design Philosophy**: Minimalist interface with focus on recipe content and readability

#### Data Processing Layer
- **Core Engine**: Llama 3.3 70B Versatile (via Groq)
- **Video Content Analysis**: Intelligent processing of cooking video transcripts
- **Recipe Structuring**: Automatic organization of ingredients, steps, and cooking parameters

#### Storage Layer
- **Technology**: Supabase (PostgreSQL-based)
- **Data Models**: User profiles, saved recipes, feedback records
- **Authentication**: Google OAuth integration

#### Translation Layer
- **Service**: Sarvam API
- **Supported Languages**: Hindi, Tamil, Gujarati, Marathi, and Bengali
- **Implementation**: Context-aware translation preserving recipe structure

## Feature Suite

### 1. Intelligent Recipe Generation
- **Video Transcript Processing**
  - Automatically extracts subtitles from YouTube cooking videos using `youtube-transcript-api`
  - Handles multilingual transcripts with translation to English when needed
  - Processes transcript content to identify recipe components
  
- **AI-Powered Structure Creation**
  - Converts unstructured video dialogue into organized recipe format
  - Identifies and categorizes ingredients with quantities
  - Sequences preparation and cooking steps in logical order
  - Extracts additional details like cooking time, difficulty, and serving size

### 2. Multilingual Support
- Delivers recipes in multiple Indian languages including Hindi, Tamil, Telugu, Kannada, Malayalam, Gujarati, Marathi, Bengali, Punjabi, Oriya, and Assamese
- Maintains formatting integrity across translations
- Allows users to switch between languages seamlessly

### 3. User Recipe Management
- **Recipe Saving**
  - Personal recipe library for authenticated users
  - Organized storage with video reference links
  - Language preference retention

- **Recipe Sharing**
  - One-click copy functionality
  - Formatted output for easy sharing

### 4. User Experience
- **Authentication System**
  - Streamlined Google login integration
  - Secure session management
  - Profile-based recipe storage

- **Feedback Collection**
  - In-app feedback submission via Streamlit interface
  - Feedback stored in Supabase database
  - Simple form-based input for user comments

## Technology Ecosystem

### Core Technologies
| Component | Technology | Purpose |
|-----------|------------|---------|
| Application Framework | Streamlit | End-to-end application delivery |
| Language Model | Llama 3.3 70B Versatile | Natural language understanding |
| Inference Platform | Groq | High-performance LLM processing |
| Database | Supabase | User data and recipe storage |
| Translation | Sarvam API | Multilingual recipe conversion |
| Video Integration | youtube-transcript-api | Subtitle extraction |
| Authentication | Supabase Auth + Google OAuth | User identity management |
| Deployment | Streamlit Cloud | Application hosting |

### Architectural Decisions

#### Why Streamlit?
Streamlit was selected for its ability to rapidly develop data-driven applications with minimal frontend expertise required. It enables quick iteration on features while providing a responsive user interface that works well for text-heavy recipe content.

#### Why Groq?
Groq's inference platform was selected for its exceptional performance in serving large language models like Llama 3.3 70B. Groq's hardware architecture is specifically designed for LLM inference, providing significantly faster response times compared to traditional GPU-based solutions. This speed advantage is crucial for YumTube's user experience, ensuring that recipe generation happens within seconds rather than minutes. Additionally, Groq's optimized API integration simplifies the development process while maintaining high throughput and low latency, which is essential when processing potentially lengthy cooking video transcripts.

#### Why Llama 3.3 70B?
This LLM was chosen for its exceptional understanding of context and instruction following, which is crucial for accurately interpreting cooking videos and structuring recipes in a natural, human-readable format.

#### Why Supabase?
Supabase provides a comprehensive backend solution that combines authentication, database, and real-time capabilities. This reduces integration complexity and allows for faster development cycles.

#### Why Sarvam API?
Sarvam excels specifically at Indian language translations, providing more culturally accurate translations of culinary terms compared to general-purpose translation APIs. It supports a comprehensive range of Indian languages, making recipes accessible to a diverse linguistic audience across India.

## User Experience Flow

1. **Language Selection**
   - User chooses preferred language from multiple supported Indian languages
   - Interface adapts to selected language

2. **Video Selection**
   - User pastes a YouTube cooking video URL
   - System validates video accessibility and subtitle availability

3. **Recipe Generation**
   - System extracts video transcript
   - LLM processes transcript into structured recipe
   - Recipe displayed with clear sections in selected language

4. **Recipe Management**
   - User can copy recipe to clipboard
   - Authenticated users can save to personal library
   - Saved recipes accessible via "Yummy Recipes" section

5. **Feedback Collection**
   - User provides application feedback
   - System stores feedback in Supabase

## Deployment Strategy

### Hosting Environment
YumTube is deployed on Streamlit Cloud, providing:
- Scalable hosting infrastructure
- Secure environment variable management
- Continuous deployment from GitHub repository

## Security Framework

### Data Protection
- API keys managed via secure environment variables
- User authentication handled through established OAuth providers
- No storage of sensitive YouTube account information

## Limitations and Boundaries

### Current Constraints
- Depends on availability of video subtitles/transcripts
- Translation quality may vary for complex culinary terms
- Recipe extraction quality depends on video narration clarity

### Edge Cases
- Very long cooking videos may require special handling
- Regional cooking techniques may not always be recognized correctly
- Videos with multiple recipes require manual separation

## Future Roadmap

### Short-term Enhancements
- Recipe image generation based on ingredients list
- Nutritional information calculation
- Shopping list export functionality

### Mid-term Vision
- Video timestamp linking to specific recipe steps
- Personalized recipe recommendations
- Dietary restriction and allergen filtering

### Long-term Expansion
- Community recipe sharing platform
- Integration with grocery delivery services
- Voice-controlled recipe navigation

## Conclusion
YumTube represents a practical application of AI to solve everyday cooking challenges. By bridging video content with structured recipes and adding multilingual support, it creates value for cooking enthusiasts across language barriers. The architecture prioritizes user experience while leveraging cutting-edge language models to deliver high-quality recipe extraction.
