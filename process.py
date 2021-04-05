import json
from datetime import datetime, time
import math

RESTRICTED_REWARD_POINTS = 1
OTHER_REWARD_POINTS = 0.25

TIMEZONE_THREE_DOLLAR = 3
TIMEZONE_TWO_DOLLAR = 2
TIMEZONE_ONE_DOLLAR = 1
OTHER_TIMEZONE = 1


class Fooda:
    # define a global user store to be used at multiple functions
    def __init__(self):
        self.user_store = {}

    # Read the input form json file
    def read_input(self):
        with open("input.json") as json_file:
            data = json.load(json_file)
        return data
    
    # Check timestamp to match the reward points
    def check_timestamp(self, time_to_check):
        # Time 12pm to 1pm
        if self.validate_timestamp(time_to_check, time(12), time(13)):
            return (TIMEZONE_THREE_DOLLAR, RESTRICTED_REWARD_POINTS)
        # Time 11am to 12pm or 1pm to 2pm
        elif self.validate_timestamp(
            time_to_check, time(11), time(12)
        ) or self.validate_timestamp(time_to_check, time(13), time(14)):
            return (TIMEZONE_TWO_DOLLAR, RESTRICTED_REWARD_POINTS)
        # Time 10am to 11am or 2pm to 3pm
        elif self.validate_timestamp(
            time_to_check, time(10), time(11)
        ) or self.validate_timestamp(time_to_check, time(14), time(15)):
            return (TIMEZONE_ONE_DOLLAR, RESTRICTED_REWARD_POINTS)
        # otherwise
        else:
            return (None, OTHER_REWARD_POINTS)

    # This functions validates it user's transaction is between timestamps
    def validate_timestamp(self, time_to_check, on_time, off_time):
        if on_time <= off_time:
            return on_time <= time_to_check < off_time
        else:  # over midnight e.g., 23:30-04:15
            return on_time <= time_to_check or time_to_check < off_time

    # This function calculate total rewards
    def calculate_reward(self, customer, amount):
        self.user_store[customer]["awarded_orders"] += 1
        self.user_store[customer]["total_rewards"] += amount
        self.user_store[customer]["average_rewards"] = math.ceil(
            self.user_store[customer]["total_rewards"]
            / self.user_store[customer]["awarded_orders"]
        )

    # This function adds reward according to timezone
    def amount_to_add(self, amount, reward_timezone, reward):
        amount_to_add = amount / reward_timezone
        final_amount = math.ceil(reward * amount_to_add)
        return final_amount
    
    # This function prints result 
    def print_result(self):
        for user, value in self.user_store.items():
            total_reward, average_reward = (
                value["total_rewards"],
                value["average_rewards"],
            )
            if total_reward == 0:
                print("{0}: No Orders.".format(user))
            else:
                print(
                    "{0}: {1} points with {2} points per order.".format(
                        user, total_reward, average_reward
                    )
                )

    def main(self):
        user_data = self.read_input()
        for user in user_data["events"]:
            if user["action"] == "new_customer":
                self.user_store[user["name"]] = {
                    "total_rewards": 0,
                    "average_rewards": 0,
                    "awarded_orders": 0,
                }
            elif user["action"] == "new_order":
                if self.user_store[user["customer"]]:

                    date_format = datetime.fromisoformat(user["timestamp"]).time()
                    timezone_reward, reward_points = self.check_timestamp(date_format)
                    if timezone_reward is not None:
                        user_amount = self.amount_to_add(
                            user["amount"],
                            timezone_reward,
                            reward_points,
                        )
                    else:
                        user_amount = math.ceil(user["amount"] * OTHER_REWARD_POINTS)
                    if 3 <= user_amount <= 20:
                        self.calculate_reward(user["customer"], user_amount)


        self.print_result()


if __name__ == "__main__":
    f = Fooda()
    f.main()