import os
import time

def cleanup_file(path):
    try:
        os.remove(path)
        print(f"[CLEANUP] Removed temporary file: {path}")
    except Exception as e:
        print(f"[CLEANUP ERROR] Failed to remove temp file: {e}")

def attach_cleanup_to_response(response, file_path, delay_if_needed=5):
    """
    Powiązuje usunięcie pliku z momentem zamknięcia odpowiedzi.

    Jeśli response ma metodę `.close()`, nadpisuje ją.
    W przeciwnym razie próbuje usunąć plik po `delay_if_needed` sekundach.
    """
    if hasattr(response, 'close'):
        original_close = response.close

        def wrapped_close():
            original_close()
            cleanup_file(file_path)

        response.close = wrapped_close
    else:
        time.sleep(delay_if_needed)
        cleanup_file(file_path)

    return response
