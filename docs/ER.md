```mermaid
erDiagram
    USERS {
        int user_id PK
        string email
        string name
    }

    PROJECTS {
        int project_id PK
        int user_id FK
        string project_name
    }

    EMAILS {
        int email_id PK
        int project_id FK
        string recipient_email
        string subject
        string sent_at
    }

    EVENTS {
        int event_id PK
        int email_id FK
        string event_type
        string location
        string user_agent
        string event_time
    }

    USERS ||--o{ PROJECTS : owns
    PROJECTS ||--o{ EMAILS : contains
    EMAILS ||--o{ EVENTS : generates
