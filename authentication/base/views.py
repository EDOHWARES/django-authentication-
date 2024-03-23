from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

questions = [
    {
        'id': 0,
        'question': 'What online resources do you use to help you do your job?',
        'hint': 'Most tech workers turn to websites such as Stack Exchange or GitHub when they need help with something. Some also have their own selection of websites, online communities, social media feeds and other resources specific to their interests. The answer to this question can indicate how engaged the candidate is with the broader IT world.'
    },
    {
        'id': 1,
        'question': 'How do you keep your technology skills current?',
        'hint': 'Tech professionals work hard to keep their knowledge base current by reading blogs and forums, taking online courses, joining hackathons and plugging away at personal IT projects. This tech interview question can help you gauge the candidate’s enthusiasm for the profession — and open a conversation about professional development.'
    },
    {
        'id': 2,
        'question': 'How would you explain [a relevant technology] to someone with limited tech skills?',
        'hint': 'IT plays a crucial role in almost every company, so communicating well with non-tech colleagues is a must. You can assess candidates’ communication skills with this question. Do they avoid obscure acronyms and jargon? How well can they break down a complicated process and compare it to something that’s common knowledge? Also, this question can help you get a feel for the candidate’s own understanding of core concepts.'
    },
    {
        'id': 3,
        'question': 'What strengths do you think are most important in a developer [or another relevant tech position]?',
        'hint': 'A question like this can reveal what the interviewee feels they can bring to the position. Some candidates may focus on technical abilities and IT certifications, while others may talk more about problem solving, attention to detail, communication and other general job skills. Look for IT candidates who give a balanced answer.'
    },
    {
        'id': 4,
        'question': 'How would your colleagues describe you?',
        'hint': 'The answer can reveal aspects of a candidate’s personality that aren’t covered on their resume. It also gives insight into how the individual perceives themself and the role they’re applying for. For example, if their answer focuses on their creative side, but the position is very analytical in nature, the job may not be a good fit.'
    }, 
    {
        'id': 5,
        'question': 'Can you tell me about a time when things didn’t go the way you wanted at work, such as a project that failed, or being passed over for a promotion?',
        'hint': 'Everyone deals with professional setbacks at some point in their career. You want to know how people handled — and what they learned from — those situations. The best employees are resilient, using setbacks as a springboard toward positive changes. So listen to not only the problem they mention but also what they did after the disappointment.'
    },
    {
        'id': 6,
        'question': 'What are your favorite and least favorite technology products, and why?',
        'hint': 'In addition to learning whether prospective employees like the hardware and software your company uses, this tech interview question helps you evaluate their enthusiasm and knowledge. Do candidates become animated when discussing the advantages and disadvantages of certain tools? Do they admire solid engineering, sleek design, intuitive user experience or another aspect of good technology? This should help determine how well they’ll mesh with your work environment.'
    }, 
    {
        'id': 7,
        'question': 'What are the benefits and the drawbacks of working in an Agile environment?',
        'hint': 'Most IT teams have adopted some form of Agile — currently the favored SDLC methodology — which means lots of quick meetings and a steady stream of feedback from fellow team members. A candidate’s answer can help you assess not only their level of understanding of this popular environment but also their attitude toward collaboration and communication.'
    },
    {
        'id': 8,
        'question': 'How do you think technology advances will impact your job?',
        'hint': 'New technology continues to change many IT roles. How aware of that is the candidate you’re interviewing? Do they know, for example, that automated testing is a major part of DevOps, which allows for faster development cycles and quicker deployment? A candidate may talk about the automation tools they use or the challenges of working with machine learning and big data. They may also discuss emerging tech, like AI, Web3, or the Metaverse. This question is a good way to start a conversation about trends and advancements in the field, and it will also give you insight into how the candidate perceives their role over the long term.'
    },
    {
        'id': 9,
        'question': 'Tell me about a tech project you’ve worked on in your spare time.',
        'hint': 'You may want to hire an IT professional who devotes personal time to side projects. Why? These are people who are driven and curious, which, in turn, keeps their skill set fresh. Ask how they stay motivated, what interests them about the project and their ultimate goal. If they can demo a website or app they’ve built, all the better.'
    }, 
    {
        'id': 10,
        'question': 'Tell us about the last presentation you gave',
        'hint': 'Today’s tech professionals can’t be lone wolves. They have to discuss changes with teammates, coordinate with other departments, advocate for platforms they prefer and much more. While not everyone has to love public speaking, your new hire should be able to conduct research, put together a solid presentation and persuade stakeholders why X is better than Y.'
    }, 
    {
        'id': 11,
        'question': 'What are the qualities of a successful team or project leader?',
        'hint': 'Always be on the lookout for leaders, even when you’re not hiring for a management position. The nature of IT work means individuals frequently have to take responsibility for delivering projects, and this requires leadership skills such as organization, motivation, positive thinking, delegation and communication. This question may also indicate how well they’ll work with your current leaders.'
    }, 
    {
        'id': 12,
        'question': 'What skills or characteristics make someone an effective remote worker?',
        'hint': 'This is an important question to ask in our pandemic-changed world. Remote workers must be self-starters who can work with little supervision. They need excellent communication abilities, as well as stellar self-discipline and time-management skills. Not everyone has those qualities, and not everyone thrives working outside an office. You want to be sure your new hire will be both productive and comfortable if working off-site.'
    },
    {
        'id': 13,
        'question': 'What would you hope to achieve in the first six months after being hired?',
        'hint': 'The answer to this tech interview question depends on the role. A developer, for example, may hope to have developed a small project during that time, while a tech manager may want to have analyzed internal processes. A candidate’s response will give you insights into their overall understanding of the position. If their goals and ambitions don’t match the job description, this may not be the right role for them.'
    }, 
    {
        'id': 14,
        'question': 'How do you handle tight deadlines?',
        'hint': 'IT teams often face daunting time constraints. You need someone who can work efficiently and accurately when under pressure. Ask this interview question of a potential employee, and you’ll at least get a sense of how they deal with stress and whether they can keep up with the pace of projects at your company. You could also follow up by asking if they’ve ever missed a deadline and, if so, how they dealt with the situation.'
    }, 
    {
        'id': 15,
        'question': 'How do you manage your work-life balance?',
        'hint': "With on-call duties and multiple pressing deadlines, some tech workers struggle with their field's always-on culture. While you want dedicated team members, you should also seek employees who can relax and take care of themselves. Burnout is a very real problem in tech, and top performers have good strategies in place to help prevent it. As a follow-up to their answer, you could talk about how your company supports a healthy work-life balance — something that can be very attractive for candidates considering multiple offers."
    }, 
    {
        'id': 16,
        'question': "Why do you want to work for us?",
        'hint': 'Individuals who truly did their homework will have done their research and be able to talk about your company’s values, products and services, and approach to technology. If they can’t articulate at least a few reasons your company would be a good match for their skills and ambitions, then they haven’t done their due diligence to properly prepare for the interview. Remember to allow time at the end of the interview for candidates to ask you questions. This is not only beneficial to applicants — it also clues you in to what matters to them. For instance, you may reconsider your interest in a prospect if they seem overly concerned about salary and vacation accrual during the first interview. Or you may be impressed when someone asks questions that demonstrate their business acumen and thorough understanding of your industry. Their answers to your questions plus the questions they ask should give you a fairly clear picture of whether you’d like to hire them or not.'
    }
]

@login_required
def home(request):
    context = {'questions': questions}
    return render(request, 'base/home.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You're successfully logged in!")
            return redirect('home')
        else:
            messages.error(request, 'An error occured, login again!')
            return redirect('login')
    return render(request, 'base/login.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('login')