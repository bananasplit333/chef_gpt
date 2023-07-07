import openai
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
openai.api_key = os.environ['OPENAI_API_KEY']

def translate(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=messages,
    )
    return response.choices[0].message["content"]


delimiter = "####"
user_prompt = f"""
    You will be given an essay. It is for a professional accountant. /
    Please summarize the essay into no more than 30 bullet points. /
    I also want you to read over the essay, and point out any grammar mistakes. /
    Also check for sentences that sound obscure or out of place./
    
    ###
    CPA PERT June 2023

    Questions

    Question 2: Solving Problems and Adding Value

    a) Describe a time when you attempted to improve a process, product or service in the workplace, including the problem you were trying to solve. What challenges did you encounter and what actions did you take to address them? Describe the CPA value that was most applicable to this situation.

    During my time as a senior associate, I noticed that our project review process was inefficient. The problem was that we lacked a centralized communication tool for team members to interact with each other, managers, and partner, leading to delayed responses and slow resolutions to the audit processes.

    My first step was to conduct a detailed analysis to understand the impact of this inefficiency. I used the feedback process and surveyed team members to gather firsthand insights into the process gaps. This analysis confirmed my hypothesis and revealed additional issues such as fragmented communication channels and a lack of abiding by review holds slotted in the team calendar.

    The challenge was convincing managers and partners about the necessity for an integrated project management platform. Despite presenting compelling details, there was some hesitation due to concerns about the time needed to implement it, the learning curve, and potential disruption to their schedules.

    To address these concerns, I organized a project plan spreadsheet and manager review list where the entire team can see the deadlines for work to be completed and when managers need to go into review. I also proposed a phased implementation plan, by first introducing the team members to follow the spreadsheet, and then eventually the managers also used their review tracker allowing for gradual adaptation and minimal disruptions. Simultaneously, I advocated for the importance of improving our process to be in line with the CPA value of professional competence and integrity. This value requires that we continually improve our operations to meet our client's needs efficiently, maintaining our professional integrity.

    Eventually, both managers and partners approved of this process. The implementation improved our process efficiency significantly, reducing review delays and increasing overall project delivery speed. This not only improve our work quality but also enhanced our reputation with clients, reflecting the CPA's emphasis on professionalism and ethics.



    b) How did you choose this course of action and what alternatives did you consider? What were the pros and cons of each alternative? How did you apply existing knowledge in new or different ways? What were the risks and limitations of your chosen course of action and how did you address them?

    Choosing this course of action was influenced by several factors. First, the survey responses and data I collected underscored the need for an integrated project plan and spreadsheet platform. This issue was causing significant inefficiencies, which was negatively impacting our deliverables and our relationships with clients. 

    I considered several alternatives. One was to continue using our current system but enforce stricter protocols for reviews. This would have minimal cost implications, but it didn't address the fundamental issue of a lack of a centralized platform. Another alternative was to develop a custom-made tool to suit our specific needs, but the cost and time of development were prohibitive. 
    The pros of the chosen solution included improving communication, enhancing efficiency, and maintaining our professional reputation. The cons were the upfront time it took to implement this, the learning curve for the team, and potential disruptions to current processes. 

    In terms of applying existing knowledge in new ways, I drew from my previous experience of transitioning to a new tool in a different organization. I used this experience to craft the phased implementation plan and address potential resistance to change among the team.

    The risks of my chosen course of action included initial resistance from team members, potential overruns in the budget due to unforeseen tasks that also require my attention and the risk that the platform might not deliver the expected benefits. 

    To address these risks, I planned training workshops to minimize resistance and made sure to involve the team in the decision-making process. For the budget, I included a buffer in the financial plan and time spent on this job to cater to any unexpected delays. As for the platform’s efficacy, I arranged for a trial period to assess its effectiveness before fully committing. 

    Ultimately, the integration of the project management platform was successful, largely due to the meticulous planning and risk mitigation strategies put in place. It was a testament to how well-thought-out decisions and risk management can lead to effective and efficient improvements in the workplace.



    c) What did you learn from this experience about solving problems? How can you apply these learnings in the future?

    This experience taught me invaluable lessons about problem-solving, the most important being the power of taking feedback and making change. I learned that it is important to speak up and think of ways to propose changes or improvements when presented with insight from the team. The feedback helped us identify the core issue and quantify its impact, making it easier to convince the team about the need for change.

    Another lesson was the importance of effective change management. Changes, especially ones involving technological shifts, can often face resistance due to the fear of the unknown. Involving team members in the decision-making process, conducting demonstration sessions, and offering training are all crucial steps in minimizing resistance and facilitating a smooth transition.

    I also learned that problem-solving often involves risk and that thorough risk assessment and mitigation strategies are key components of any decision-making process. By anticipating potential problems and preparing for them, we can prevent minor hitches from becoming major roadblocks.
    In the future, I'll continue to apply these learnings when addressing workplace challenges. I will leverage feedback to support my decisions, ensure effective change management when introducing new processes or tools, and always consider potential risks and mitigation strategies. Moreover, I will persistently reflect on the CPA value of professional competence and integrity to guide my actions, maintaining the highest standards of integrity and continually striving for operational efficiency to best serve our clients.

    Question 3: Communicating 

    a) Describe a time when you adapted your oral or written communication to meet the needs of a specific audience. What actions did you take? Describe the CPA value that was most applicable to this situation.

    During my time as a senior associate, I was assigned to audit a real estate company. The company's staff was older and familiar with general business terms, but they lacked deep knowledge of financial audit processes and their terminology. The challenge was to effectively communicate our audit process and findings to them in a way that would be both understandable and valuable for their business.
    I adapted my communication style by simplifying audit jargon and incorporating more real estate-related analogies, aligning my language more closely with their domain. I made sure to explain why each audit step was essential, its relevance to their business, and what the implications of our findings were.

    To ensure that the written communication was also easily understandable, I created visual aids like flowcharts and infographics to explain the audit process and findings. We also organized regular meetings where we explained the audit stages and outcomes and gave them a chance to ask questions.

    Throughout this process, I was guided by the CPA value of professional competence and due care. This principle emphasizes the need to ensure that clients understand the services provided to them, even if it requires going beyond standard procedures or practices. By modifying my communication to meet the needs of the client, I was demonstrating this value, ensuring that they fully understood the audit process, its relevance, and the results.

    This adaptation not only helped build a stronger relationship with the client but also led to the client taking a more active role in understanding their financial controls and how they could improve them, reflecting the true value of an audit beyond just compliance.


    b) How did you choose this course of action and what alternatives did you consider? What were the pros and cons of each alternative? What would have been the result had you not taken these steps?

    Choosing this course of action involved a careful assessment of the client's knowledge gaps and communication style. I considered their familiarity with real estate language and noticed a lack of understanding regarding financial audit jargon. I recognized that it was my responsibility to bridge this gap and ensure the audit process was valuable to them.

    The alternatives included sticking to the standard language and procedures used in auditing, or, on the other extreme, completely watering down the audit process and jargon. 

    The pros of sticking to standard audit language were that it would maintain the precision and accuracy that comes with the technical terminology. The cons were that the client might not understand the process, making it less valuable for them. This could lead to disengagement, ineffective audits, or possible compliance issues down the line.

    On the other hand, watering down the audit process and jargon would have made it easier for the client to understand. However, the cons of this approach included the risk of oversimplification, potentially making the audit process appear less robust, and leading to misunderstandings about the importance of certain steps or controls.

    Balancing these alternatives, I chose a middle ground. I used simplified language and real estate-related analogies without losing the essence of the audit process. This approach was chosen as it promised to maintain the integrity of the audit while making it understandable and relevant for the client.

    Had I not taken these steps, the communication gap might have persisted. The client could have remained disengaged and unable to leverage the audit findings to improve their financial controls, which would have resulted in a missed opportunity for their growth. Moreover, it could have strained our relationship with them, making future collaborations difficult. By adapting my communication, I managed to foster a stronger relationship with the client and made the audit process a valuable learning experience for them.



    c) What did you learn from this experience about communicating? How can you apply these learnings in the future?

    From this experience, I learned that effective communication is not about sticking rigidly to technical jargon or established norms, but about understanding the listener's perspective and tailoring your message to their needs and level of understanding. Simplifying complex ideas and using relatable analogies can go a long way in making the message more understandable and relevant.

    This experience emphasized the importance of visual aids in communication. Visuals like flowcharts and infographics can help simplify complex processes and findings, making them more accessible to audiences unfamiliar with audit jargon.

    I also learned the value of interactive communication. Regular meetings provided a platform for the client to ask questions and for us to explain concepts, creating an environment of mutual understanding.

    In the future, these learnings can be applied in multiple ways. First, I'll continue to adjust my communication style based on my audience's background and understanding, whether they're clients from different industries or non-financial colleagues within my own organization. Second, I'll make more extensive use of visual aids when explaining complex processes or findings. Finally, I'll prioritize interactive communication, encouraging questions and discussion to ensure understanding and engagement.

    Ultimately, this experience reinforced the idea that effective communication is about clarity, relevance, and engagement, and these principles will guide my communication strategy in the future.














    Question 4: Managing Self

    a) Describe a time when your performance did not fully meet your expectations. What challenges did you encounter and what actions did you take to address them? Describe the CPA value that was most applicable to this situation.

    There was a time as a senior associate when I was leading the audit of a real estate client. Given the size and complexity of the client's operations, the task was more challenging than I had anticipated. There were also issues with resource management and the staffing for my team kept changing and we switched managers 3 times. Despite my best efforts, there were instances where we fell behind schedule and struggled to meet certain deadlines. 

    One of the main challenges was that the audit team was relatively inexperienced and needed more guidance and support than I had initially anticipated. Additionally, I underestimated the time it would take to review the complex real estate valuation and depreciation assessments that this client required.

    Recognizing these challenges, I took several steps to address them. Firstly, I invested more time in mentoring and training the junior associates on the team to enhance their understanding and speed up their work. Secondly, I sought help from more experienced colleagues to better understand the complexities of the real estate valuation assessments. Finally, I worked extra hours to make up for the lost time and ensure we were back on track.

    The CPA value that was most applicable in this situation was professional competence and due care. This value emphasizes the responsibility of the CPA to maintain a high level of professional knowledge and skill, and to act diligently in the best interests of the client. By investing time in training my team and seeking help to understand complex issues, I was practicing due diligence and ensuring that we had the competence necessary to carry out the audit.

    While the outcome wasn't as smooth as I had hoped, it was a significant learning experience for me. It taught me the importance of assessing team capabilities and client complexities more accurately. I now incorporate these learnings into my planning for each audit, ensuring a more realistic schedule and better resource allocation.



    b) When you reflect on your course of action, what alternatives could you have considered? What were the pros and cons of each alternative? Who could you have consulted with or sought guidance from?

    Upon reflecting, there were a few alternative courses of action I could have considered.

    Firstly, I could have requested additional resources from the start. The pros of this approach would have been to distribute the workload more evenly, making the process more manageable and less likely to run into delays. The con would have been the potential increase in costs for the client and the firm, and the risk of overcomplicating the project with too many team members.

    Secondly, I could have requested to bring in a more experienced team member earlier to handle the complex real estate valuation assessments. The pro would have been more accurate and quicker assessments. The con would have been a potentially higher cost due to the involvement of more senior personnel, and it might have seemed like I was unable to handle the responsibility given to me.

    Finally, I could have insisted on more comprehensive pre-audit planning. This would have allowed me to better understand the client's operations and anticipate the complexities. The pro would have been a smoother audit process and potentially fewer delays. The con might have been that it would take more time upfront, potentially delaying the start of the audit.

    As for guidance, I could have consulted with the engagement partner or previous managers, who would have more experience with managing large and complex audits. I could also have reached out to peers who had experience with similar clients or audits to learn from their experiences and best practices.

    In retrospect, a combination of these alternatives would likely have led to a more efficient audit. However, the experience served as a valuable lesson for me about the importance of thorough planning, understanding team dynamics, and asking for help when necessary. These insights have since improved my performance in subsequent audits.

    c) Having carried out these actions, what would you do differently next time? What skills do you need to develop to help you meet your expectations going forward in your career? How are you planning to gain them?

    Through this experience, there are a few things I would do differently if this situation were to happen again. 

    Firstly, I would conduct more comprehensive pre-audit planning, which would involve thoroughly understanding the client's business, operations, and unique complexities. A deeper understanding of the client's specifics would enable me to anticipate potential hurdles and plan for them. This would help me hone in on my project management skills and better oversee the entire audit process, manage resources effectively, and anticipate and mitigate potential risks.

    Secondly, I would assess the capabilities and experience level of my team more accurately at the outset. If the team lacks experience in certain areas, I would request additional support or arrange for relevant training beforehand. I would also look at the time allocation each member has to ensure they have time for coaching and are able to complete all tasks assigned. This would help me improve my leadership skills, which would allow me to better guide my team, manage their workload, and mentor junior associates, leading to more efficient audits.

    Finally, I would improve my communication with the engagement partner or manager, keeping them more informed about the progress and potential challenges we are facing. This could open up avenues for additional guidance and support when necessary.










    Question A
    Identify key competency areas (enabling and/or technical) you will focus on developing or improving between now and your next meeting with your mentor. What is your action plan for doing so?


    Moving forward, I aim to focus on my technical skills as I will be leading audits and guiding team members over various tasks. As I begin leading engagements, I will also be working closely with managers and parters, so I will need to continue working on my communication skills and make sure I keep everyone up to date on the file. I will continue to ask for feedback to ensure I am striving towards improvement and meeting the goals I’ve set with my managers.



    Question B
    Looking back at your experience captured in this report, in which competency areas (enabling or technical) do you feel most confident in your abilities and why?

    I feel most confident in my professinoal compentency and due care as I was able to effectively lead a team, resolve issues, and add value to the engagement. I believe I put my best foot forward and considered many approaches before taking action to ensure an optimal outcome. Having gone through the challenges of new engagement, working with team members of varying skills, and implementing a better process, I’ve learned hard skills that I will use as a guide for my future decisions.
    ####
"""

print(translate(user_prompt))