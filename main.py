from mmpd.process.ProcessFlow import ProcessFlow

def main():
    process = ProcessFlow('Test Process')
    step_0 = process.add_step()
    step_1 = process.add_step()
    next = process.step_next_step()

    print(next.index)

if __name__ == '__main__':
    main()