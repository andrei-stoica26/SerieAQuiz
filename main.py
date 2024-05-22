import os
import save_data
import generate_questions
import write_js

def main():
    if not os.path.exists('Data'):
        save_data.main()
    generate_questions.main()
    write_js.main()

if __name__ == '__main__':
    main()
