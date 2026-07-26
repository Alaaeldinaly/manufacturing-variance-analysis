import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class ManufacturingBIAnalyzer:
    """
    Business Intelligence Analyzer for Hybrid Manufacturing Datasets.
    Performs Schedule Variance Analysis and Operational Bottleneck Identification.
    """

    def __init__(self, data_path: str, output_dir: str = "outputs"):
        self.data_path = data_path
        self.output_dir = output_dir
        self.df = None

        # Ensure output directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def load_and_clean_data(self):
        """Load data, parse datetimes, and compute schedule variance metrics."""
        print("[1/4] Loading and parsing manufacturing dataset...")
        self.df = pd.read_csv(self.data_path)

        # Parse datetime columns
        datetime_cols = [
            "Scheduled_Start",
            "Scheduled_End",
            "Actual_Start",
            "Actual_End",
        ]
        for col in datetime_cols:
            self.df[col] = pd.to_datetime(self.df[col])

        # Calculate Start Delay (Start Lag) in minutes
        self.df["Start_Delay_Min"] = (
            self.df["Actual_Start"] - self.df["Scheduled_Start"]
        ).dt.total_seconds() / 60.0

        # Calculate Scheduled vs Actual Duration
        self.df["Scheduled_Duration_Min"] = (
            self.df["Scheduled_End"] - self.df["Scheduled_Start"]
        ).dt.total_seconds() / 60.0
        self.df["Actual_Duration_Min"] = (
            self.df["Actual_End"] - self.df["Actual_Start"]
        ).dt.total_seconds() / 60.0
        self.df["Duration_Variance_Min"] = (
            self.df["Actual_Duration_Min"] - self.df["Scheduled_Duration_Min"]
        )

        print("[SUCCESS] Data preprocessing complete.")

    def generate_executive_summary(self):
        """Generate executive metrics summary for Board of Directors presentation."""
        print("\n[2/4] Generating Executive Summary...")
        total_jobs = len(self.df)
        status_counts = self.df["Job_Status"].value_counts()

        df_valid = self.df.dropna(subset=["Start_Delay_Min"])

        delayed_jobs = df_valid[df_valid["Job_Status"] == "Delayed"]
        avg_delay = delayed_jobs["Start_Delay_Min"].mean()

        print("=" * 60)
        print(" EXECUTIVE SUMMARY: SCHEDULE VARIANCE & PERFORMANCE")
        print("=" * 60)
        print(f"Total Jobs Analyzed:              {total_jobs}")
        print(
            f"Completed Jobs:                   {status_counts.get('Completed', 0)} ({status_counts.get('Completed', 0)/total_jobs:.1%})"
        )
        print(
            f"Delayed Jobs:                     {status_counts.get('Delayed', 0)} ({status_counts.get('Delayed', 0)/total_jobs:.1%})"
        )
        print(
            f"Failed Jobs:                      {status_counts.get('Failed', 0)} ({status_counts.get('Failed', 0)/total_jobs:.1%})"
        )
        print(f"Average Start Delay (Delayed):   {avg_delay:.2f} Minutes")
        print("=" * 60)

    def analyze_machine_bottlenecks(self):
        """Analyze job failure and delay distributions per machine."""
        print("\n[3/4] Analyzing Machine Performance Metrics (%) ...")
        machine_summary = (
            self.df.groupby("Machine_ID")["Job_Status"]
            .value_counts(normalize=True)
            .unstack()
            * 100
        )
        print(machine_summary.round(2))

    def export_distribution_chart(self):
        """Generate and save Schedule Variance Distribution Plot."""
        print("\n[4/4] Exporting Chart Visualizations...")
        df_valid = self.df.dropna(subset=["Start_Delay_Min"])

        plt.figure(figsize=(11, 5))
        sns.histplot(
            data=df_valid,
            x="Start_Delay_Min",
            hue="Job_Status",
            bins=30,
            kde=True,
            palette="Set2",
        )

        plt.title(
            "Schedule Variance Analysis: Start Delay (Minutes) by Job Status",
            fontsize=12,
            pad=15,
        )
        plt.xlabel("Start Delay (Minutes)", fontsize=10)
        plt.ylabel("Count of Jobs", fontsize=10)
        plt.axvline(
            0, color="black", linestyle="--", label="On-Time Threshold (0 Min)"
        )
        plt.legend()
        plt.tight_layout()

        chart_path = os.path.join(
            self.output_dir, "schedule_variance_distribution.png"
        )
        plt.savefig(chart_path, dpi=300)
        plt.close()
        print(f"[SUCCESS] Chart saved to: {chart_path}")


if __name__ == "__main__":
    # Path to input file
    DATA_FILE = "hybrid_manufacturing_categorical.csv"

    # Initialize and execute pipeline
    analyzer = ManufacturingBIAnalyzer(data_path=DATA_FILE)
    analyzer.load_and_clean_data()
    analyzer.generate_executive_summary()
    analyzer.analyze_machine_bottlenecks()
    analyzer.export_distribution_chart()