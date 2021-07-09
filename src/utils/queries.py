def insert_query():
    return "INSERT INTO urls (original_url) VALUES (?)"


def get_query():
    return "SELECT original_url, clicks FROM urls" " WHERE id = (?)"


def update_click_query():
    return "UPDATE urls SET clicks = ? WHERE id = ?"
