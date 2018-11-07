import mapping


def main():
    filename = input("Enter filename: ")
    data = open("data/"+filename, "r")
    map = mapping.Map(data)
    map.printDetails()
    data.close()

if __name__ == "__main__": main()
