from mmpd.process.ProcessStep import ProcessStep

class PreProduct:
    __process_steps: set[ProcessStep]

    def add_to_step(self, step: ProcessStep) -> None:
        if step in self.__process_steps:
            raise ValueError('PreProduct already in this step')
        
        self.__process_steps.add(step)