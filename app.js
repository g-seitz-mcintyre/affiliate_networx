document.addEventListener('DOMContentLoaded', function() {
    const nextBtn = document.getElementById('next-btn');
    const prevBtn = document.getElementById('prev-btn');
    const submitBtn = document.getElementById('submit-btn');
    const surveyQuestions = [
        {
            section: "Section 1: Channel Integration and Consistency",
            questions: [
                {
                    question: "Can customers return online purchases in physical stores?",
                    options: ["Yes, always", "Yes, but with limitations", "No", "Not applicable/No physical stores"],
                    scores: [3, 2, 1, 0]
                },
                {
                    question: "Is inventory visible and shared across online and physical stores?",
                    options: ["Yes, in real-time", "Yes, with some delays", "No", "Not applicable/No physical stores"],
                    scores: [3, 2, 1, 0]
                },
                {
                    question: "Do you offer consistent product pricing and promotions across all channels?",
                    options: ["Yes, always", "Mostly, with occasional exceptions", "No, pricing and promotions vary significantly between channels"],
                    scores: [3, 2, 1]
                }
            ]
        },
        {
            section: "Section 2: Customer Experience Across Channels",
            questions: [
                {
                    question: "Can customers use loyalty points and rewards across all channels?",
                    options: ["Yes, seamlessly", "Yes, but with some restrictions", "No"],
                    scores: [3, 2, 1]
                },
                {
                    question: "How do you rate your company's ability to provide a seamless transition from online to in-store experiences (e.g., buy online, pick up in-store)?",
                    options: ["Excellent", "Good", "Fair", "Poor"],
                    scores: [3, 2, 1, 0]
                },
                {
                    question: "Are customer service channels integrated to provide a unified view of customer interactions (e.g., a customer service representative can see online and in-store purchase history)?",
                    options: ["Yes, fully integrated", "Partially integrated", "No"],
                    scores: [3, 2, 1]
                }
            ]
        },
        {
            section: "Section 3: Data Analytics and Personalization",
            questions: [
                {
                    question: "Do you utilize customer data from all channels to personalize marketing communications and offers?",
                    options: ["Yes, extensively", "To some extent", "No"],
                    scores: [3, 2, 1]
                },
                {
                    question: "Is there a centralized customer data platform that aggregates data across all channels?",
                    options: ["Yes", "In progress", "No"],
                    scores: [3, 2, 1]
                }
            ]
        },
        {
            section: "Section 4: Technology and Innovation",
            questions: [
                {
                    question: "How would you rate your company's adoption of emerging technologies (e.g., mobile apps, AI, AR/VR) to enhance the omni-channel experience?",
                    options: ["Leading edge", "Competitive", "Emerging", "Behind"],
                    scores: [3, 2, 1, 0]
                }
            ]
        }
    ];

    const form = document.getElementById('survey-form');
    let currentSectionIndex = 0;
    const totalSections = surveyQuestions.length;

    initSurvey();
    updateNavigation();

    nextBtn.addEventListener('click', function() {
        if (currentSectionIndex < totalSections - 1) {
            currentSectionIndex++;
            updateSectionVisibility();
            updateNavigation();
        }
    });

    prevBtn.addEventListener('click', function() {
        if (currentSectionIndex > 0) {
            currentSectionIndex--;
            updateSectionVisibility();
            updateNavigation();
        }
    });

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        let totalScore = 0;
        const formData = new FormData(form);
        for (let value of formData.values()) {
            totalScore += parseInt(value, 10);
        }
        displayResults(totalScore);
    });

    function initSurvey() {
        surveyQuestions.forEach((section, sectionIndex) => {
            const sectionDiv = document.createElement('div');
            sectionDiv.classList.add('survey-section', 'mb-8');
            sectionDiv.style.display = sectionIndex === 0 ? 'block' : 'none';

            const sectionTitle = document.createElement('h2');
            sectionTitle.classList.add('text-xl', 'font-bold', 'mb-4');
            sectionTitle.textContent = section.section;
            sectionDiv.appendChild(sectionTitle);

            section.questions.forEach((question, questionIndex) => {
                const questionEl = document.createElement('fieldset');
                questionEl.classList.add('mb-6');
                const questionLegend = document.createElement('legend');
                questionLegend.classList.add('font-semibold');
                questionLegend.textContent = question.question;
                questionEl.appendChild(questionLegend);

                question.options.forEach((option, optionIndex) => {
                    const label = document.createElement('label');
                    label.classList.add('block', 'cursor-pointer', 'mb-2');
                    const input = document.createElement('input');
                    input.type = 'radio';
                    input.name = `question-${sectionIndex}-${questionIndex}`;
                    input.value = question.scores[optionIndex];
                    label.appendChild(input);
                    label.append(` ${option}`);
                    questionEl.appendChild(label);
                });

                sectionDiv.appendChild(questionEl);
            });

            form.insertBefore(sectionDiv, form.querySelector('#navigation-buttons'));
        });
    }

    function updateSectionVisibility() {
        document.querySelectorAll('.survey-section').forEach((section, index) => {
            section.style.display = index === currentSectionIndex ? 'block' : 'none';
        });
    }

    function updateNavigation() {
        prevBtn.style.display = currentSectionIndex > 0 ? 'inline-block' : 'none';
        nextBtn.style.display = currentSectionIndex < totalSections - 1 ? 'inline-block' : 'none';
        submitBtn.style.display = currentSectionIndex === totalSections - 1 ? 'inline-block' : 'none';
    }

    function displayResults(score) {
        const classification = classifyScore(score);
        window.location.href = `results.html?score=${score}&classification=${classification}`;
    }

    function classifyScore(score) {
        // Adjust classification thresholds as needed
        if (score >= 20) return 'Advanced';
        else if (score >= 10) return 'Intermediate';
        else return 'Beginner';
    }
});
