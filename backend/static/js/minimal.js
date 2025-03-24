document.getElementById('mainBadger').addEventListener('mouseenter', () => {
    document.querySelectorAll('.orbit').forEach(orbit => {
        orbit.style.animationPlayState = 'paused';
    });
});

document.getElementById('mainBadger').addEventListener('mouseleave', () => {
    document.querySelectorAll('.orbit').forEach(orbit => {
        orbit.style.animationPlayState = 'running';
    });
});