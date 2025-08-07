// Countdown Timer Functionality
function updateCountdown() {
    const targetDate = new Date();
    targetDate.setDate(targetDate.getDate() + 1);
    targetDate.setHours(12, 25, 6, 0);
    
    const now = new Date().getTime();
    const distance = targetDate.getTime() - now;
    
    if (distance > 0) {
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);
        
        updateTimeUnit('days', days.toString().padStart(2, '0'));
        updateTimeUnit('hours', hours.toString().padStart(2, '0'));
        updateTimeUnit('minutes', minutes.toString().padStart(2, '0'));
        updateTimeUnit('seconds', seconds.toString().padStart(2, '0'));
    } else {
        document.getElementById('days').textContent = '00';
        document.getElementById('hours').textContent = '00';
        document.getElementById('minutes').textContent = '00';
        document.getElementById('seconds').textContent = '00';
    }
}

function updateTimeUnit(id, value) {
    const element = document.getElementById(id);
    if (element.textContent !== value) {
        element.style.animation = 'none';
        element.offsetHeight;
        element.style.animation = 'countdownPulse 2s ease-in-out infinite';
        element.textContent = value;
    }
}

function showLevelTooltip(element, level, prize) {
    const tooltip = document.getElementById('levelTooltip');
    const tooltipLevel = document.getElementById('tooltipLevel');
    const tooltipPrize = document.getElementById('tooltipPrize');
    
    tooltipLevel.textContent = `Level : ${level}`;
    tooltipPrize.textContent = `Prize : ${prize}`;
    
    // Position the tooltip relative to the level circle
    const levelRect = element.getBoundingClientRect();
    const tooltipRect = tooltip.getBoundingClientRect();
    
    // Center by default
    let leftPos = levelRect.left + (levelRect.width / 2) - (tooltipRect.width / 2);
    let bottomPos = 165;
    
    // Adjust for left edge cases
    if (leftPos < 10) {
        tooltip.classList.add('left-align');
        leftPos = 10;
    } 
    // Adjust for right edge cases
    else if (leftPos + tooltipRect.width > window.innerWidth - 10) {
        tooltip.classList.add('right-align');
        leftPos = window.innerWidth - tooltipRect.width - 10;
    } else {
        tooltip.classList.remove('left-align', 'right-align');
    }
    
    // Apply the positions
    tooltip.style.left = `${leftPos}px`;
    tooltip.style.bottom = `${bottomPos}px`;
    tooltip.style.display = 'flex';
}

function hideLevelTooltip() {
    const tooltip = document.getElementById('levelTooltip');
    tooltip.style.display = 'none';  
}

// Level unlock functionality
function unlockLevel(element, level) {
    if (element.classList.contains('locked')) {
        element.classList.remove('locked');
        element.classList.add('unlocked');
        
        // Show unlock icon and hide lock icon
        const lockIcon = element.querySelector('.lock-icon');
        const unlockIcon = element.querySelector('.unlock-icon');
        if (lockIcon && unlockIcon) {
            lockIcon.style.display = 'none';
            unlockIcon.style.display = 'block';
        }
        
        
        // Update status text
        const status = element.querySelector('.level-status');
        if (status) {
            status.textContent = 'Unlocked!';
        }
        
        // Add stars
        const starsContainer = element.parentElement.querySelector('.level-stars');
        if (starsContainer) {
            starsContainer.innerHTML = '';
            for (let i = 0; i < 5; i++) {
                const star = document.createElement('span');
                star.className = 'star-icon';
                star.textContent = '★';
                starsContainer.appendChild(star);
            }
            starsContainer.style.display = 'flex';
        }
        
        // Update next connector line
        const nextConnector = element.closest('.level-item').querySelector('.level-connector');
        if (nextConnector) {
            nextConnector.style.background = '#E6A063';
            nextConnector.style.height = '3px';
        }
        
        alert(`Level ${level} unlocked successfully!`);
    } else {
        alert(`Level ${level} is already unlocked!`);
    }
}
// Sidebar menu interactions
function toggleMenu(element) {
    const expandIcon = element.querySelector('.expand-icon');
    if (expandIcon) {
        const isExpanded = expandIcon.style.transform === 'rotate(180deg)';
        expandIcon.style.transform = isExpanded ? 'rotate(0deg)' : 'rotate(180deg)';
        element.style.background = isExpanded ? 'transparent' : '#f0f0f0';
        setTimeout(() => {
            element.style.background = 'transparent';
        }, 200);
    }
}

// Initialize everything when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Start countdown timer
    updateCountdown();
    setInterval(updateCountdown, 1000);
    
    // Show level tooltip for Level 01 after 3 seconds
    setTimeout(() => {
        const level01 = document.querySelector('.level-item:nth-child(1)');
        if (level01) {
            showLevelTooltip(level01, '01', '35200');
        }
    }, 3000);
    
    // Add click handlers for expandable menu items
    document.querySelectorAll('.menu-item.expandable').forEach(item => {
        item.addEventListener('click', () => toggleMenu(item));
    });
    
    // Add click handlers for buttons
    document.querySelector('.participate-btn').addEventListener('click', function() {
        this.style.transform = 'scale(0.95)';
        setTimeout(() => {
            this.style.transform = 'translateY(-2px)';
        }, 150);
        alert('Redirecting to participation form...');
    });
    
    document.querySelector('.submit-art-btn').addEventListener('click', function() {
        alert('Opening art submission form...');
    });
    
    document.querySelector('.enroll-btn').addEventListener('click', function() {
        alert('Enrolling in selected level...');
        hideLevelTooltip();
    });
    
    // Add menu item click handlers
    document.querySelectorAll('.menu-item:not(.expandable)').forEach(item => {
        item.addEventListener('click', function() {
            const menuText = this.querySelector('.menu-text').textContent.trim();
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
            console.log(`Clicked on: ${menuText}`);
        });
    });
    
    // Add hover effect for refer button
    const referBtn = document.querySelector('.refer-btn');
    if (referBtn) {
        referBtn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-1px)';
            this.style.boxShadow = '0 4px 12px rgba(74, 144, 226, 0.3)';
        });
        
        referBtn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
    }
    
    // Add smooth scrolling for levels container
    const levelsContainer = document.querySelector('.levels-container');
    if (levelsContainer) {
        let isDown = false;
        let startX;
        let scrollLeft;

        levelsContainer.addEventListener('mousedown', (e) => {
            isDown = true;
            levelsContainer.classList.add('active');
            startX = e.pageX - levelsContainer.offsetLeft;
            scrollLeft = levelsContainer.scrollLeft;
        });

        levelsContainer.addEventListener('mouseleave', () => {
            isDown = false;
            levelsContainer.classList.remove('active');
        });

        levelsContainer.addEventListener('mouseup', () => {
            isDown = false;
            levelsContainer.classList.remove('active');
        });

        levelsContainer.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - levelsContainer.offsetLeft;
            const walk = (x - startX) * 2;
            levelsContainer.scrollLeft = scrollLeft - walk;
        });
    }
    
    // Add keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            hideLevelTooltip();
        }
        
        const levelsContainer = document.querySelector('.levels-container');
        if (levelsContainer) {
            if (e.key === 'ArrowLeft') {
                levelsContainer.scrollLeft -= 100;
            } else if (e.key === 'ArrowRight') {
                levelsContainer.scrollLeft += 100;
            }
        }
    });
});

// Add parallax effect to banner illustration
document.addEventListener('mousemove', function(e) {
    const bannerIllustration = document.querySelector('.banner-illustration img');
    if (bannerIllustration) {
        const rect = bannerIllustration.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        const deltaX = (e.clientX - centerX) / 200;
        const deltaY = (e.clientY - centerY) / 200;
        
        bannerIllustration.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
    }
});

document.addEventListener('mouseleave', function() {
    const bannerIllustration = document.querySelector('.banner-illustration img');
    if (bannerIllustration) {
        bannerIllustration.style.transform = 'translate(0px, 0px)';
    }
});