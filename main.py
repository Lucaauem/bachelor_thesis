from mmpd.process.ProcessFlow import ProcessFlow

def main():
    process = ProcessFlow('Test Process')
    print(process.name)

if __name__ == '__main__':
    main()