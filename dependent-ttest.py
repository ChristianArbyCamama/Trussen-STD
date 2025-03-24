import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from data import (
    control_pretest_scores,
    control_posttest_scores,
    experimental_pretest_scores,
    experimental_posttest_scores,
)

class DependentTtest:
    def __init__(self):
        # Significance level (two-tailed)
        self.alpha = 0.05

    def calculate_critical_value(self, alpha, df):
        self.critical_value = stats.t.ppf(1 - alpha / 2, df)

    def compute_dependent_ttest(self, pretest_scores, posttest_scores):
        # Perform the dependent t-test
        result = stats.ttest_rel(posttest_scores, pretest_scores)

        self.statistic = result.statistic
        self.pvalue = result.pvalue
        self.degree_of_freedom = result.df

        self.calculate_critical_value(self.alpha, self.degree_of_freedom)
        self.mean_difference = np.mean(
            posttest_scores - pretest_scores
        )  # Mean difference

    def display_dependent_ttest_result(
        self, pretest_scores, posttest_scores, group_name
    ):
        self.group_name = group_name
        self.pretest_scores = pretest_scores
        self.posttest_scores = posttest_scores

        self.compute_dependent_ttest(self.pretest_scores, self.posttest_scores)

        print()
        print(f"*" * 50, end="\n\n")
        print(f"{group_name} Result")
        print(f"Mean difference: {self.mean_difference}")
        print(f"T-statistic: {self.statistic}")
        print(f"P-value: {self.pvalue}")
        print(f"Degree of freedom: {self.degree_of_freedom}")
        print(f"Critical-value: {self.critical_value}")

        ###
        # The first method compares the absolute value of the test statistic (calculated from your data)
        # to a critical value, which is based on the chosen significance level (𝛼) and the degrees of freedom.
        # If the test statistic exceeds the critical value, you reject the null hypothesis.
        ###
        if abs(self.statistic) > self.critical_value:
            print("\nstatistic > critical value: Reject the null hypothesis.")
        else:
            print("\nstatistic <= critical value: Fail to reject the null hypothesis.")

        ###
        # The second method uses the p-value, which is the probability of obtaining a test statistic at least
        # as extreme as the one observed, assuming the null hypothesis is true. If the p-value is less than
        # or equal to your significance level (𝛼), you reject the null hypothesis.
        ###
        if abs(self.pvalue) <= self.alpha:
            print("pvalue <= alpha: Reject the null hypothesis.")
        else:
            print("pvalue > alpha: Fail to reject the null hypothesis.")

        # Determine if it is positive, negative, or no siginificant difference in performance
        if self.mean_difference > 0:
            print(f"Performance improved for {self.group_name} (Positive Change).")
        elif self.mean_difference < 0:
            print(f"Performance declined for {self.group_name} (Negative Change).")
        else:
            print("No change in performance.")

    def plot_result(self):
        # Calculate the differences
        # differences = self.pretest_scores - self.posttest_scores

        plt.plot(self.pretest_scores, "r-o")
        plt.plot(self.posttest_scores, "b-o")
        plt.yticks(range(min(self.pretest_scores), max(self.posttest_scores) + 1, 1))
        plt.title(f"{self.group_name} Dependent T-Test Result")
        plt.legend(["Pretest", "Posttest"])
        plt.ylabel("Score")
        plt.xlabel("Students")
        plt.show()

# Control Group Data
control_pretest_scores = np.array(control_pretest_scores)
control_posttest_scores = np.array(control_posttest_scores)

# Experimental Group Data
experimental_pretest_scores = np.array(experimental_pretest_scores)
experimental_posttest_scores = np.array(experimental_posttest_scores)

# Perform the dependent t-test for control group
control_ttest = DependentTtest()
control_ttest.display_dependent_ttest_result(
    control_pretest_scores, control_posttest_scores, "Control Group"
)
control_ttest.plot_result()

# Perform the dependent t-test for control group
experimental_ttest = DependentTtest()
experimental_ttest.display_dependent_ttest_result(
    experimental_pretest_scores, experimental_posttest_scores, "Experimental Group"
)
experimental_ttest.plot_result()
