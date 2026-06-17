from candidate import Candidate
from voter import Voter
from queue import Queue

import random


class VotingSystem:
    def __init__(self):
        self.candidates = []
        self.voters = []

    def num_candidates(self):
        while True:
            total = int(
                input(
                    "Please enter the amount of candidates you want "
                    "to be included in the RCV: "
                )
            )

            if 0 < total <= 13:
                return total

    def build_rankings(self):
        """Build a ranking queue for each voter based on political distance."""
        rankings = {}

        for voter in self.voters:
            ranked_candidates = sorted(
                self.candidates,
                key=lambda candidate: abs(voter.leaning - candidate.get_leaning())
            )

            # Queue stores the voter's preferences in order:
            # first choice at the front, then second choice, etc.
            ranking_queue = Queue()

            for candidate in ranked_candidates:
                ranking_queue.enqueue(candidate.get_name())

            rankings[voter.id] = ranking_queue

        return rankings

    def voting_results(self):
        rankings = self.build_rankings()
        active_candidates = {
            candidate.get_name()
            for candidate in self.candidates
        }

        round_number = 1

        while True:
            vote_counts = {
                candidate: 0
                for candidate in active_candidates
            }

            for ranking_queue in rankings.values():
                while (
                    not ranking_queue.is_empty()
                    and ranking_queue.peek() not in active_candidates
                ):
                # Remove eliminated candidates until the voter has
                # an active candidate at the front of their ranking.
                    ranking_queue.dequeue()

                if not ranking_queue.is_empty():
                    top_choice = ranking_queue.peek()
                    vote_counts[top_choice] += 1

            total_votes = sum(vote_counts.values())

            print(f"\nRound {round_number} results:")

            for candidate, votes in sorted(vote_counts.items()):
                percentage = (votes / total_votes) * 100
                print(f"{candidate}: {percentage:.2f}% ({votes} votes)")

            for candidate, votes in vote_counts.items():
                if votes > total_votes / 2:
                    print(f"\nWinner: {candidate}")
                    return candidate

            eliminated_candidate = min(
                vote_counts,
                key=lambda candidate: (vote_counts[candidate], candidate)
            )
            # Ties for fewest votes are broken alphabetically by candidate name.

            print(f"Eliminated: {eliminated_candidate}")

            active_candidates.remove(eliminated_candidate)
            round_number += 1

    def generate_candidates(self, count):
        names = [
            'Aang', 'Katara', 'Sokka', 'Zuko', 'Iroh',
            'Appa', 'Momo', 'Toph', 'Azula', 'Suki',
            'Ozai', 'Mai', 'Ty'
        ]

        self.candidates = [
            Candidate(
                name=names[i],
                leaning=random.uniform(-1.0, 1.0)
            )
            for i in range(count)
        ]

    def generate_voters(self, count):
        self.voters = [
            Voter(
                id=i + 1,
                leaning=random.uniform(-1.0, 1.0)
            )
            for i in range(count)
        ]


if __name__ == "__main__":
    voting_system = VotingSystem()

    total = voting_system.num_candidates()

    voting_system.generate_candidates(total)
    voting_system.generate_voters(100)

    print("Candidates:")
    for candidate in voting_system.candidates:
        print(candidate)

    print("\nVoters:")
    for voter in voting_system.voters:
        print(voter)

    voting_system.voting_results()