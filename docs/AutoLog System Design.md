```mermaid
sequenceDiagram
    autonumber
    participant AppA as Device A (App)
    participant AppB as Device B (App)
    participant Server
    participant Redis
    participant DB as User DB (email, user_id, refresh_token)
    participant GoogleOAuth

    %% First login on Device A
    AppA->>GoogleOAuth: OAuth login
    GoogleOAuth-->>AppA: ID token
    AppA->>Server: Send ID token
    Server->>DB: Check if email exists
    alt Email not in DB
        DB-->>Server: Create user_id, store email + refresh_token
    else Email exists
        DB-->>Server: Return user_id, update refresh_token
    end
    Server->>Redis: Generate session_token -> user_id
    Redis-->>Server: Store mapping
    Server-->>AppA: Return session_token
    AppA-->>AppA: Store session_token locally (secure storage)

    %% Auto-login on Device A
    AppA->>Server: Send session_token
    Server->>Redis: Lookup session_token
    Redis-->>Server: Return user_id
    Server-->>AppA: Authorize & return data

    %% Login on Device B
    AppB->>GoogleOAuth: OAuth login
    GoogleOAuth-->>AppB: ID token
    AppB->>Server: Send ID token
    Server->>DB: Check if email exists
    DB-->>Server: Return user_id, update refresh_token
    Server->>Redis: Generate session_token_B -> same user_id
    Redis-->>Server: Store mapping
    Server-->>AppB: Return session_token_B
    AppB-->>AppB: Store session_token locally

    %% After 14 days
    Server->>Redis: Expire session_token(s)
    Redis-->>Server: Session tokens removed
    GoogleOAuth-->>Server: Refresh token expired
    Server-->>App: Redirect to OAuth login
