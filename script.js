document.addEventListener('DOMContentLoaded', () => {
    
    // Initialize Lucide Icons
    lucide.createIcons();

    // Global Language State
    let currentLang = 'en';

    // --- Translation Dictionary ---
    const translations = {
        en: {
            brandName: "Agri-Safe",
            navFeatures: "Features",
            navMarket: "Market Prices",
            navHowItWorks: "How it Works",
            navLogin: "Login",
            heroTitle1: "Smart Farming,",
            heroTitle2: "Simplified.",
            heroSub: "Scan your crops for diseases and get safe, weather-aware advice in your own language.",
            btnScan: "Scan Crop",
            btnVoice: "Voice Assistant",
            mandiTitle: "Today's Mandi Prices",
            mandiUpdate: "Updated 1 hr ago",
            cropWheat: "Wheat (Gehu)",
            cropRice: "Rice (Dhaan)",
            cropSugar: "Sugarcane",
            cropMustard: "Mustard",
            perQtl: "/ qtl",
            feat1Title: "Weather-Smart Spraying",
            feat1Desc: "If rain is coming, we'll tell you to wait before spraying pesticides, saving you money and effort.",
            feat2Title: "Local Language Chat",
            feat2Desc: "Talk to our AI assistant using voice or text in your native language for verified agricultural advice.",
            footerText: "Empowering Farmers with AI",
            modalTitle: "Welcome Back",
            modalSub: "Login with your mobile number",
            modalLabel: "Mobile Number",
            modalPlaceholder: "Enter 10 digit number",
            modalBtn: "Get OTP",
            verifyBtn: "Verify & Login",
            editNumber: "Edit mobile number",
            toastListen: "Listening... Speak now",
            
            // Alert Strings
            alertScanTitle: "Image Captured",
            alertScanMsg: "Your crop image has been successfully captured and is ready for AI analysis.",
            alertVoiceTitle: "Voice Captured",
            alertVoiceMsg: "Your question has been recorded. The assistant is processing your request.",
            alertInvalidNumTitle: "Invalid Number",
            alertInvalidNumMsg: "Please enter a genuine 10-digit Indian mobile number (must start with 6, 7, 8, or 9)."
        },
        hi: {
            brandName: "एग्री-सेफ",
            navFeatures: "विशेषताएं",
            navMarket: "मंडी के भाव",
            navHowItWorks: "यह कैसे काम करता है",
            navLogin: "लॉग इन",
            heroTitle1: "स्मार्ट खेती,",
            heroTitle2: "अब और भी आसान।",
            heroSub: "बीमारियों के लिए अपनी फसलों को स्कैन करें और अपनी भाषा में मौसम-आधारित सुरक्षित सलाह पाएं।",
            btnScan: "फसल स्कैन करें",
            btnVoice: "वॉयस असिस्टेंट",
            mandiTitle: "आज के मंडी भाव",
            mandiUpdate: "1 घंटे पहले अपडेट किया गया",
            cropWheat: "गेहूँ",
            cropRice: "धान",
            cropSugar: "गन्ना",
            cropMustard: "सरसों",
            perQtl: "/ क्विंटल",
            feat1Title: "मौसम-अनुकूल छिड़काव",
            feat1Desc: "अगर बारिश होने वाली है, तो हम आपको कीटनाशक छिड़कने से पहले रुकने की सलाह देंगे, जिससे आपके पैसे और मेहनत बचेगी।",
            feat2Title: "स्थानीय भाषा में चैट",
            feat2Desc: "सत्यापित कृषि सलाह के लिए अपनी मूल भाषा में वॉयस या टेक्स्ट का उपयोग करके हमारे AI सहायक से बात करें।",
            footerText: "AI के साथ किसानों को सशक्त बनाना",
            modalTitle: "वापसी पर स्वागत है",
            modalSub: "अपने मोबाइल नंबर से लॉग इन करें",
            modalLabel: "मोबाइल नंबर",
            modalPlaceholder: "10 अंकों का नंबर दर्ज करें",
            modalBtn: "OTP प्राप्त करें",
            verifyBtn: "सत्यापित करें और लॉग इन करें",
            editNumber: "मोबाइल नंबर बदलें",
            toastListen: "सुन रहा हूँ... अब बोलें",

            // Alert Strings
            alertScanTitle: "छवि कैप्चर की गई",
            alertScanMsg: "आपकी फसल की छवि सफलतापूर्वक कैप्चर कर ली गई है और AI विश्लेषण के लिए तैयार है।",
            alertVoiceTitle: "आवाज़ कैप्चर की गई",
            alertVoiceMsg: "आपका प्रश्न रिकॉर्ड कर लिया गया है। सहायक आपके अनुरोध पर कार्रवाई कर रहा है।",
            alertInvalidNumTitle: "अमान्य नंबर",
            alertInvalidNumMsg: "कृपया 10 अंकों का सही भारतीय मोबाइल नंबर दर्ज करें (6, 7, 8 या 9 से शुरू होना चाहिए)।"
        }
    };

    // --- Custom Alert Logic ---
    const customAlert = document.getElementById('custom-alert');
    const alertTitle = document.getElementById('alert-title');
    const alertMessage = document.getElementById('alert-message');
    const alertIconContainer = document.getElementById('alert-icon-container');
    const alertIcon = document.getElementById('alert-icon');
    const closeAlertBtn = document.getElementById('close-alert-btn');

    function showCustomAlert(title, message, type = 'success') {
        alertTitle.innerText = title;
        alertMessage.innerText = message;

        // Reset styling
        alertIconContainer.className = "mx-auto w-16 h-16 rounded-full flex items-center justify-center mb-4";
        
        if (type === 'success') {
            alertIconContainer.classList.add('bg-green-100', 'text-agriGreen');
            alertIcon.setAttribute('data-lucide', 'check-circle');
            closeAlertBtn.className = "w-full bg-agriGreen hover:bg-agriDark text-white font-bold py-3 rounded-lg transition shadow-md";
        } else if (type === 'error') {
            alertIconContainer.classList.add('bg-red-100', 'text-red-600');
            alertIcon.setAttribute('data-lucide', 'alert-triangle');
            closeAlertBtn.className = "w-full bg-red-600 hover:bg-red-700 text-white font-bold py-3 rounded-lg transition shadow-md";
        }

        lucide.createIcons(); // Refresh the icon
        customAlert.classList.remove('hidden');
    }

    closeAlertBtn.addEventListener('click', () => {
        customAlert.classList.add('hidden');
    });

    // --- Language Selector Logic ---
    const langSelectors = document.querySelectorAll('.lang-selector');
    
    function updateLanguage(lang) {
        currentLang = lang;
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (translations[lang][key]) el.innerText = translations[lang][key];
        });
        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            const key = el.getAttribute('data-i18n-placeholder');
            if (translations[lang][key]) el.placeholder = translations[lang][key];
        });
        langSelectors.forEach(s => s.value = lang);
        document.documentElement.lang = lang;
    }

    langSelectors.forEach(selector => {
        selector.addEventListener('change', (e) => updateLanguage(e.target.value));
    });


    // --- Mobile Menu Logic ---
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');

    mobileMenuBtn.addEventListener('click', () => mobileMenu.classList.toggle('hidden'));
    mobileMenu.querySelectorAll('a').forEach(link => link.addEventListener('click', () => mobileMenu.classList.add('hidden')));

    // --- Login Modal & OTP Logic ---
    const loginModal = document.getElementById('login-modal');
    const loginForm = document.getElementById('login-form');
    const otpForm = document.getElementById('otp-form');
    const mobileInput = document.getElementById('mobile-input');
    const displayMobileNum = document.getElementById('display-mobile-num');
    
    // Buttons
    const desktopLoginBtn = document.getElementById('login-btn-desktop');
    const mobileLoginBtn = document.getElementById('login-btn-mobile');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const backToMobileBtn = document.getElementById('back-to-mobile-btn');
    const verifyBtn = document.getElementById('verify-btn');

    function openModal() { 
        loginModal.classList.remove('hidden'); 
        resetLoginFlow();
    }
    
    function closeModal() { loginModal.classList.add('hidden'); }

    function resetLoginFlow() {
        loginForm.classList.remove('hidden');
        otpForm.classList.add('hidden');
        mobileInput.value = '';
        document.getElementById('modal-title').innerText = translations[currentLang].modalTitle;
        document.getElementById('modal-subtitle').innerText = translations[currentLang].modalSub;
        document.getElementById('modal-header-icon').setAttribute('data-lucide', 'smartphone');
        lucide.createIcons();
    }

    desktopLoginBtn.addEventListener('click', openModal);
    mobileLoginBtn.addEventListener('click', openModal);
    closeModalBtn.addEventListener('click', closeModal);
    backToMobileBtn.addEventListener('click', resetLoginFlow);

    loginModal.addEventListener('click', (e) => {
        if (e.target === loginModal) closeModal();
    });

    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const mobileNum = mobileInput.value.trim();
        
        // Feature 1: If empty, bypass validation and redirect to OTP screen directly
        if (mobileNum === "") {
            switchToOtpScreen("Test Mode (No Number)");
            return;
        }

        // Feature 2: Strict genuine 10-digit Indian number validation
        // Must start with 6, 7, 8, or 9 and be exactly 10 digits long.
        const mobileRegex = /^[6-9]\d{9}$/;
        if (!mobileRegex.test(mobileNum)) {
            showCustomAlert(
                translations[currentLang].alertInvalidNumTitle, 
                translations[currentLang].alertInvalidNumMsg, 
                'error'
            );
            return;
        }

        // If valid, switch to OTP screen
        switchToOtpScreen("+91 " + mobileNum);
    });

    function switchToOtpScreen(numberDisplay) {
        loginForm.classList.add('hidden');
        otpForm.classList.remove('hidden');
        displayMobileNum.innerText = numberDisplay;
        
        document.getElementById('modal-title').innerText = currentLang === 'en' ? "Enter OTP" : "OTP दर्ज करें";
        document.getElementById('modal-subtitle').innerText = currentLang === 'en' ? "Secure Verification" : "सुरक्षित सत्यापन";
        document.getElementById('modal-header-icon').setAttribute('data-lucide', 'shield-check');
        lucide.createIcons();
    }

    // Verify OTP simulation
    verifyBtn.addEventListener('click', () => {
        closeModal();
        showCustomAlert(
            currentLang === 'en' ? "Login Successful" : "लॉग इन सफल", 
            currentLang === 'en' ? "Welcome back to Agri-Safe." : "एग्री-सेफ में आपका स्वागत है।"
        );
    });

    // --- Scan Crop (Camera/File Upload) Logic ---
    const scanCropBtn = document.getElementById('scan-crop-btn');
    const cameraInput = document.getElementById('camera-input');

    scanCropBtn.addEventListener('click', () => cameraInput.click());

    cameraInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            showCustomAlert(translations[currentLang].alertScanTitle, translations[currentLang].alertScanMsg);
            cameraInput.value = ''; 
        }
    });

    // --- Voice Assistant Logic ---
    const voiceBtn = document.getElementById('voice-btn');
    const voiceToast = document.getElementById('voice-toast');
    let isListening = false;
    let voiceTimeout;

    voiceBtn.addEventListener('click', () => {
        if (isListening) return;

        isListening = true;
        voiceToast.classList.remove('hidden');
        
        voiceTimeout = setTimeout(() => {
            voiceToast.classList.add('hidden');
            showCustomAlert(translations[currentLang].alertVoiceTitle, translations[currentLang].alertVoiceMsg);
            isListening = false;
        }, 3000);
    });

});