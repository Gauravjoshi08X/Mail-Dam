```mermaid
erDiagram
    USER {
        int user_id PK
        string email
        string name
        datetime created_at
    }

    PROJECT {
        int project_id PK
        int user_id FK
        string project_name
        datetime created_at
    }

    EMAIL {
        int email_id PK
        int project_id FK
        string recipient_email
        string subject
        datetime sent_at
    }

    EVENT {
        int event_id PK
        int email_id FK
        string event_type
        string location
        string user_agent
        datetime event_time
    }

    USER ||--o{ PROJECT : owns
    PROJECT ||--o{ EMAIL : contains
    EMAIL ||--o{ EVENT : generates
