from ProcessStep import ProcessStep

class Operator:
    __process_steps: set[ProcessStep]

    def add_to_step(self, step: ProcessStep) -> None:
        if step in self.__process_steps:
            raise ValueError('Operator already in this step')
        
        self.__process_steps.add(step)
