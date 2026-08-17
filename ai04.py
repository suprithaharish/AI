class RuleBasedSystem:
    def __init__(self, facts, rules):
        self.facts = set(facts)
        self.rules = rules

    def forward_chain(self):
        iterations = 0

        while True:
            new_fact_added = False

            for rule in self.rules:
                # Check if all conditions of the rule exist in current facts
                if all(cond in self.facts for cond in rule['if']):
                    if rule['then'] not in self.facts:
                        print(
                            f"Rule Triggered: IF {rule['if']} "
                            f"THEN Add {rule['then']}"
                        )

                        self.facts.add(rule['then'])
                        new_fact_added = True

            if not new_fact_added:
                break

            iterations += 1

        return self.facts


# Example Usage
if __name__ == "__main__":

    # Base facts
    initial_facts = [
        'Socrates_is_human',
        'All_humans_are_mortal'
    ]

    # Production rules
    production_rules = [
        {
            'if': [
                'Socrates_is_human',
                'All_humans_are_mortal'
            ],
            'then': 'Socrates_is_mortal'
        }
    ]

    # Create Rule-Based System object
    rbs = RuleBasedSystem(
        initial_facts,
        production_rules
    )

    print("Initial Facts:", initial_facts)

    # Perform forward chaining
    final_kb = rbs.forward_chain()

    print("Final Knowledge Base Facts:", final_kb)