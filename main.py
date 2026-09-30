import pandas as pd
import matplotlib.pyplot as plt
import os

# ============================================================
# PROJECT: IT SUPPORT COST OPTIMIZATION USING DATA ANALYSIS
# ============================================================

print("=" * 65)
print(" IT SUPPORT COST OPTIMIZATION USING DATA ANALYSIS")
print("=" * 65)


# ============================================================
# STEP 1: LOAD DATASET
# ============================================================

file_path = "data/customer_support_tickets.csv"

df = pd.read_csv(file_path)

print("\nSTEP 1: DATASET INFORMATION")
print("-" * 45)

print("Dataset Shape:", df.shape)

print("\nColumn Names:")
print(df.columns.tolist())


# ============================================================
# STEP 2: MISSING VALUE ANALYSIS
# ============================================================

print("\nSTEP 2: MISSING VALUES")
print("-" * 45)

missing_values = df.isnull().sum()

print(missing_values)


# ============================================================
# STEP 3: DUPLICATE CHECK
# ============================================================

print("\nSTEP 3: DUPLICATE CHECK")
print("-" * 45)

duplicate_ids = df["Ticket ID"].duplicated().sum()

print("Duplicate Ticket IDs:", duplicate_ids)


# ============================================================
# STEP 4: DATA CLEANING
# ============================================================

print("\nSTEP 4: DATA CLEANING")
print("-" * 45)

# Remove personal information and long text
clean_df = df.drop(
    columns=[
        "Customer Name",
        "Customer Email",
        "Ticket Description"
    ],
    errors="ignore"
).copy()


# Convert date/time columns
date_columns = [
    "Date of Purchase",
    "First Response Time",
    "Time to Resolution"
]

for col in date_columns:

    if col in clean_df.columns:

        clean_df[col] = pd.to_datetime(
            clean_df[col],
            errors="coerce"
        )


# Convert satisfaction rating to numeric
clean_df["Customer Satisfaction Rating"] = pd.to_numeric(
    clean_df["Customer Satisfaction Rating"],
    errors="coerce"
)


print("Cleaned Dataset Shape:", clean_df.shape)

print("\nMissing Values After Cleaning:")
print(clean_df.isnull().sum())


# ============================================================
# STEP 5: TICKET STATUS ANALYSIS
# ============================================================

print("\nSTEP 5: TICKET STATUS ANALYSIS")
print("-" * 45)

status_counts = clean_df["Ticket Status"].value_counts()

print(status_counts)

status_percentage = (
    status_counts / len(clean_df) * 100
).round(2)

print("\nPercentage of Tickets by Status:")
print(status_percentage)


# ============================================================
# STEP 6: TICKET TYPE ANALYSIS
# ============================================================

print("\nSTEP 6: TICKET TYPE ANALYSIS")
print("-" * 45)

ticket_type_counts = clean_df["Ticket Type"].value_counts()

print("\nTickets by Type:")
print(ticket_type_counts)

ticket_type_percentage = (
    ticket_type_counts / len(clean_df) * 100
).round(2)

print("\nPercentage by Ticket Type:")
print(ticket_type_percentage)


# ============================================================
# STEP 7: PRIORITY ANALYSIS
# ============================================================

print("\nSTEP 7: TICKET PRIORITY ANALYSIS")
print("-" * 45)

priority_counts = clean_df["Ticket Priority"].value_counts()

print(priority_counts)

priority_percentage = (
    priority_counts / len(clean_df) * 100
).round(2)

print("\nPriority Percentages:")
print(priority_percentage)


# ============================================================
# STEP 8: CUSTOMER SATISFACTION ANALYSIS
# ============================================================

print("\nSTEP 8: CUSTOMER SATISFACTION ANALYSIS")
print("-" * 45)

satisfaction = clean_df.dropna(
    subset=["Customer Satisfaction Rating"]
)

print(
    "Tickets with Satisfaction Ratings:",
    len(satisfaction)
)

overall_satisfaction = (
    satisfaction["Customer Satisfaction Rating"].mean()
)

print(
    "Overall Average Satisfaction:",
    round(overall_satisfaction, 2)
)


# Satisfaction by Ticket Type
satisfaction_by_type = (
    satisfaction
    .groupby("Ticket Type")[
        "Customer Satisfaction Rating"
    ]
    .mean()
    .sort_values(ascending=False)
)

print("\nAverage Satisfaction by Ticket Type:")
print(satisfaction_by_type.round(2))


# Satisfaction by Priority
satisfaction_by_priority = (
    satisfaction
    .groupby("Ticket Priority")[
        "Customer Satisfaction Rating"
    ]
    .mean()
    .sort_values(ascending=False)
)

print("\nAverage Satisfaction by Priority:")
print(satisfaction_by_priority.round(2))


# ============================================================
# STEP 9: CLOSED TICKET ANALYSIS
# ============================================================

print("\nSTEP 9: CLOSED TICKET ANALYSIS")
print("-" * 45)

closed = clean_df[
    clean_df["Ticket Status"] == "Closed"
].copy()

print("Total Closed Tickets:", len(closed))

print("\nClosed Tickets by Priority:")
closed_by_priority = closed["Ticket Priority"].value_counts()
print(closed_by_priority)

print("\nClosed Tickets by Type:")
closed_by_type = closed["Ticket Type"].value_counts()
print(closed_by_type)

print("\nMissing Resolution Timestamps in Closed Tickets:")

print(
    closed["Time to Resolution"].isnull().sum()
)

print("\nResolution Timestamp Range:")

print(
    "Earliest:",
    closed["Time to Resolution"].min()
)

print(
    "Latest:",
    closed["Time to Resolution"].max()
)

print(
    "\nNote: Resolution duration is not calculated because "
    "ticket creation timestamps are not available."
)


# ============================================================
# STEP 10: FIRST RESPONSE ANALYSIS
# ============================================================

print("\nSTEP 10: FIRST RESPONSE TIME ANALYSIS")
print("-" * 45)

first_response = clean_df.dropna(
    subset=["First Response Time"]
)

print(
    "Tickets with First Response Timestamp:",
    len(first_response)
)

print("\nFirst Response Timestamp Range:")

print(
    "Earliest:",
    first_response["First Response Time"].min()
)

print(
    "Latest:",
    first_response["First Response Time"].max()
)

print(
    "\nNote: Actual response duration cannot be calculated "
    "because ticket creation timestamps are unavailable."
)


# ============================================================
# STEP 11: TICKET TYPE VS STATUS
# ============================================================

print("\nSTEP 11: TICKET TYPE VS STATUS ANALYSIS")
print("-" * 45)

type_status = pd.crosstab(
    clean_df["Ticket Type"],
    clean_df["Ticket Status"]
)

print("\nTicket Type vs Ticket Status:")
print(type_status)


# Open + Pending
open_pending = type_status[
    ["Open", "Pending Customer Response"]
].copy()

open_pending["Total Unresolved"] = (
    open_pending["Open"]
    + open_pending["Pending Customer Response"]
)

open_pending = open_pending.sort_values(
    "Total Unresolved",
    ascending=False
)

print("\nOpen + Pending Tickets by Type:")
print(open_pending)


# Unresolved percentage
total_by_type = clean_df["Ticket Type"].value_counts()

unresolved_percentage = (
    open_pending["Total Unresolved"]
    / total_by_type.loc[open_pending.index]
    * 100
).round(2)

print("\nUnresolved Ticket Percentage by Type:")
print(unresolved_percentage)


# ============================================================
# STEP 12: TICKET CHANNEL ANALYSIS
# ============================================================

print("\nSTEP 12: TICKET CHANNEL ANALYSIS")
print("-" * 45)

channel_counts = clean_df["Ticket Channel"].value_counts()

print("\nTickets by Channel:")
print(channel_counts)

channel_percentage = (
    channel_counts / len(clean_df) * 100
).round(2)

print("\nPercentage of Tickets by Channel:")
print(channel_percentage)


print("\nTicket Channel vs Ticket Status:")

channel_status = pd.crosstab(
    clean_df["Ticket Channel"],
    clean_df["Ticket Status"]
)

print(channel_status)


# ============================================================
# STEP 13: PRIORITY VS STATUS
# ============================================================

print("\nSTEP 13: PRIORITY VS STATUS ANALYSIS")
print("-" * 45)

priority_status = pd.crosstab(
    clean_df["Ticket Priority"],
    clean_df["Ticket Status"]
)

print("\nTicket Priority vs Ticket Status:")
print(priority_status)


priority_unresolved = priority_status[
    ["Open", "Pending Customer Response"]
].copy()

priority_unresolved["Total Unresolved"] = (
    priority_unresolved["Open"]
    + priority_unresolved["Pending Customer Response"]
)

priority_unresolved = priority_unresolved.sort_values(
    "Total Unresolved",
    ascending=False
)

print("\nUnresolved Tickets by Priority:")
print(priority_unresolved)


# ============================================================
# STEP 14: OVERALL WORKLOAD ANALYSIS
# ============================================================

print("\nSTEP 14: OVERALL WORKLOAD ANALYSIS")
print("-" * 45)

total_tickets = len(clean_df)

total_closed = (
    clean_df["Ticket Status"] == "Closed"
).sum()

total_open = (
    clean_df["Ticket Status"] == "Open"
).sum()

total_pending = (
    clean_df["Ticket Status"]
    == "Pending Customer Response"
).sum()

total_unresolved = total_open + total_pending

unresolved_percentage_overall = (
    total_unresolved / total_tickets * 100
)

print("Total Tickets:", total_tickets)

print("Closed Tickets:", total_closed)

print("Open Tickets:", total_open)

print("Pending Tickets:", total_pending)

print("Total Unresolved Tickets:", total_unresolved)

print(
    "Overall Unresolved Percentage:",
    round(unresolved_percentage_overall, 2),
    "%"
)


# ============================================================
# STEP 15: CREATE OUTPUT FOLDER
# ============================================================

print("\nSTEP 15: SAVING RESULTS")
print("-" * 45)

os.makedirs("output", exist_ok=True)


# Save cleaned dataset
clean_df.to_csv(
    "output/cleaned_customer_support_tickets.csv",
    index=False
)

print(
    "Cleaned dataset saved successfully!"
)


# ============================================================
# VISUALIZATION 1: TICKETS BY TYPE
# ============================================================

plt.figure(figsize=(10, 6))

ticket_type_counts.plot(
    kind="bar",
    edgecolor="black"
)

plt.title(
    "Number of Customer Support Tickets by Type"
)

plt.xlabel("Ticket Type")

plt.ylabel("Number of Tickets")

plt.xticks(
    rotation=30,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    "output/tickets_by_type.png",
    dpi=300
)

plt.show()


# ============================================================
# VISUALIZATION 2: TICKETS BY PRIORITY
# ============================================================

plt.figure(figsize=(8, 6))

priority_counts.plot(
    kind="bar",
    edgecolor="black"
)

plt.title(
    "Number of Customer Support Tickets by Priority"
)

plt.xlabel("Ticket Priority")

plt.ylabel("Number of Tickets")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    "output/tickets_by_priority.png",
    dpi=300
)

plt.show()


# ============================================================
# VISUALIZATION 3: SATISFACTION BY TYPE
# ============================================================

plt.figure(figsize=(10, 6))

satisfaction_by_type.plot(
    kind="bar",
    edgecolor="black"
)

plt.title(
    "Average Customer Satisfaction by Ticket Type"
)

plt.xlabel("Ticket Type")

plt.ylabel("Average Satisfaction Rating")

plt.xticks(
    rotation=30,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    "output/satisfaction_by_ticket_type.png",
    dpi=300
)

plt.show()


# ============================================================
# VISUALIZATION 4: TICKET STATUS
# ============================================================

plt.figure(figsize=(8, 6))

status_counts.plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90
)

plt.title(
    "Ticket Status Distribution"
)

plt.ylabel("")

plt.tight_layout()

plt.savefig(
    "output/ticket_status.png",
    dpi=300
)

plt.show()


# ============================================================
# VISUALIZATION 5: TICKET CHANNEL
# ============================================================

plt.figure(figsize=(8, 6))

channel_counts.plot(
    kind="bar",
    edgecolor="black"
)

plt.title(
    "Customer Support Tickets by Channel"
)

plt.xlabel("Ticket Channel")

plt.ylabel("Number of Tickets")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    "output/tickets_by_channel.png",
    dpi=300
)

plt.show()


# ============================================================
# VISUALIZATION 6: UNRESOLVED TICKETS BY TYPE
# ============================================================

plt.figure(figsize=(10, 6))

open_pending["Total Unresolved"].plot(
    kind="bar",
    edgecolor="black"
)

plt.title(
    "Unresolved Tickets by Ticket Type"
)

plt.xlabel("Ticket Type")

plt.ylabel("Open + Pending Tickets")

plt.xticks(
    rotation=30,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    "output/unresolved_tickets_by_type.png",
    dpi=300
)

plt.show()


# ============================================================
# FINAL PROJECT SUMMARY
# ============================================================

print("\n" + "=" * 65)

print("FINAL PROJECT SUMMARY")

print("=" * 65)

print(
    "\nTotal Tickets:",
    total_tickets
)

print(
    "Total Closed Tickets:",
    total_closed
)

print(
    "Total Open Tickets:",
    total_open
)

print(
    "Total Pending Tickets:",
    total_pending
)

print(
    "Total Unresolved Tickets:",
    total_unresolved
)

print(
    "Overall Unresolved Percentage:",
    round(
        unresolved_percentage_overall,
        2
    ),
    "%"
)

print(
    "Average Customer Satisfaction:",
    round(
        overall_satisfaction,
        2
    )
)

print("\nTop Ticket Type by Volume:")

print(
    ticket_type_counts.idxmax(),
    "-",
    ticket_type_counts.max(),
    "tickets"
)

print("\nHighest Unresolved Workload by Type:")

print(
    open_pending["Total Unresolved"].idxmax(),
    "-",
    open_pending["Total Unresolved"].max(),
    "tickets"
)

print("\nAll analysis completed successfully!")

print(
    "Cleaned dataset and visualizations "
    "are saved in the output folder."
)

print("=" * 65)