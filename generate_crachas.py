import apis.api_csv as api_csv
import apis.api_recognition as api_recognition


def main():

    print('')

    dataframe = api_csv.load_csv()
    api_recognition.generate_cracha(dataframe)


if __name__ == "__main__":
    main()
