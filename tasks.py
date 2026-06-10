from crewai import Task
from agents import coverage_analyst, pricing_optimizer, merchant_comms

coverage_analysis_task = Task(
    description="""
    Analyse the merchant performance data located at '/Users/nishakshitij/Desktop/AI Builds/ai_d8/data/merchants.csv'.
    
    Your job is to:
    1. Read all merchant data using the read_merchant_data tool
    2. Identify merchants where order frequency is declining across all 3 weeks
    3. For each declining merchant, calculate their severity score using the 
       calculate_severity_score tool
    4. Identify the root cause pattern — is this a courier reliability issue 
       (high SLA breach rate) or a demand issue (low orders but acceptable SLA)?
    5. Write a structured report covering all findings
    
    A merchant is considered declining if Week 3 orders are lower than Week 1 orders.
    Pay special attention to merchants with SLA breach rates above 0.25.
    """,
    expected_output="""
    A structured report with exactly these four sections:
    
    EXECUTIVE SUMMARY
    - Total merchants analysed
    - Number of declining merchants found
    - Number flagged as CRITICAL or HIGH severity
    
    DECLINING MERCHANTS (one entry per merchant)
    - Merchant name and ID
    - Zone
    - Order trend (Week 1 → Week 2 → Week 3)
    - Severity score and label
    - Root cause: courier reliability or demand issue
    - Recommended action
    
    STABLE MERCHANTS
    - Brief list of merchants not requiring intervention
    
    TOP 3 PRIORITY MERCHANTS
    - The 3 merchants needing immediate action, ranked by severity score
    """,
    agent=coverage_analyst
)

pricing_optimization_task = Task(
    description="""
    You will receive a coverage analysis report from the Coverage Analyst.
    
    Your job is to:
    1. Read the TOP 3 PRIORITY MERCHANTS from the report
    2. For each priority merchant, design the optimal incentive:
       - If root cause is courier reliability: recommend operational fix first, 
         coupon second — discounting on top of bad service doesn't work
       - If root cause is demand: recommend a time-limited coupon sized to 
         recover order frequency without over-spending
    3. For coupon recommendations, show the ROI case:
       - Assume average order value of Rs 350
       - Assume platform margin of 18%
       - Calculate: at what order recovery rate does the coupon pay for itself?
    4. Segment merchants by courier type (BYOC vs Platform) — 
       the intervention strategy differs by type
    """,
    expected_output="""
    A pricing recommendation document with exactly these sections:
    
    BYOC MERCHANTS — RECOMMENDATIONS
    - Merchant name
    - Root cause summary
    - Recommended intervention (operational or coupon)
    - If coupon: amount, duration, ROI breakeven point
    
    PLATFORM MERCHANTS — RECOMMENDATIONS  
    - Same structure as above
    
    COST SUMMARY
    - Total coupon spend if all recommendations accepted
    - Expected order recovery if interventions work
    - ROI timeline (weeks to breakeven)
    """,
    agent=pricing_optimizer,
    context=[coverage_analysis_task]
)

merchant_comms_task = Task(
    description="""
    You will receive the coverage analysis report and pricing recommendations.
    
    Your job is to write one personalised outreach email per priority merchant.
    
    Rules for every email:
    1. Reference something specific about that merchant's actual situation — 
       their zone, their order numbers, their courier type
    2. Never mention that you ran an algorithm or analysis on their data —
       it should feel like a human noticed their situation
    3. Lead with acknowledgment of their challenge, not with the offer
    4. The offer (coupon or operational fix) comes in the second paragraph
    5. Keep each email under 150 words
    6. Tone: warm, direct, specific — not corporate, not salesy
    """,
    expected_output="""
    One complete email per priority merchant with:
    
    Subject line: specific to their situation, not generic
    
    Email body:
    - Paragraph 1: acknowledge their specific situation (zone, order drop, 
      delivery time if relevant)
    - Paragraph 2: the offer — specific coupon amount or operational action
    - Paragraph 3: one clear call to action
    
    After all emails, a brief DRAFTING NOTES section:
    - What personalisation hook you used for each merchant
    - Why you chose that hook over others available in the data
    """,
    agent=merchant_comms,
    context=[coverage_analysis_task, pricing_optimization_task]
)