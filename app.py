import sys
from embed_stego import embed_message
from extract_stego import read_embedded_message


def print_usage():
    print("Usage:")
    print('  Embed:  python3 app.py embed input.jpeg output.jpeg "secret text"')
    print("  Extract: python3 app.py extract stego.jpeg")


def main_cli(argv):
    if len(argv) < 2:
        print_usage()
        return 1

    cmd = argv[1].lower()
    if cmd == "embed":
        if len(argv) != 5:
            print_usage()
            return 1
        cover_image_filepath = argv[2]
        stego_image_filepath = argv[3]
        secret = argv[4]
        embed_message(cover_image_filepath, stego_image_filepath, secret)
        return 0

    elif cmd == "extract":
        if len(argv) != 3:
            print_usage()
            return 1
        stego_image = argv[2]
        message = read_embedded_message(stego_image)
        print("Extracted message:")
        print(message)
        return 0

    else:
        print_usage()
        return 1


if __name__ == "__main__":
    sys.exit(main_cli(sys.argv))
