from backend.database import get_connection
import json
from backend.encryption import (
    encrypt_text,
    decrypt_text
)

def save_credential(
    website,
    username,
    password,
    metadata
):
    conn = get_connection()
    cursor = conn.cursor()
    password = encrypt_text(password)
    encrypted_metadata = {}

    for key, value in metadata.items():
        encrypted_metadata[key] = (
            encrypt_text(value)
        )

    metadata_json = json.dumps(
        encrypted_metadata
    )

    cursor.execute("""
        INSERT INTO credentials (
            website,
            username,
            password,
            metadata
        )
        VALUES (?, ?, ?, ?)
    """, (
        website,
        username,
        password,
        metadata_json
    ))

    conn.commit()
    conn.close()


def get_all_websites():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT website
        FROM credentials
        ORDER BY website
    """)

    websites = [row[0] for row in cursor.fetchall()]

    conn.close()

    return websites


def get_credential_by_website(website):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            username,
            password,
            metadata
        FROM credentials
        WHERE website = ?
    """, (website,))

    result = cursor.fetchone()

    conn.close()

    if result:
        username, password, metadata_json = result
        password = decrypt_text(password)

        metadata = {}

        if metadata_json:
            encrypted_metadata = json.loads(
                metadata_json
            )

            metadata = {}

            for key, value in encrypted_metadata.items():
                metadata[key] = decrypt_text(value)

        return (
            username,
            password,
            metadata
        )

    return None

def delete_credential(website):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM credentials
        WHERE website = ?
    """, (website,))

    conn.commit()
    conn.close()

def update_credential(
    old_website,
    new_website,
    username,
    password,
    metadata
):
    conn = get_connection()
    cursor = conn.cursor()

    encrypted_metadata = {}

    for key, value in metadata.items():
        encrypted_metadata[key] = (
            encrypt_text(value)
        )

    metadata_json = json.dumps(
        encrypted_metadata
    )
    password = encrypt_text(password)
    
    cursor.execute("""
        UPDATE credentials
        SET
            website = ?,
            username = ?,
            password = ?,
            metadata = ?
        WHERE website = ?
    """, (
        new_website,
        username,
        password,
        metadata_json,
        old_website
    ))

    conn.commit()
    conn.close()