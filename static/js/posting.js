document.addEventListener('DOMContentLoaded', () => {
    const postForm = document.getElementById('post-form');
    const postResult = document.getElementById('post-result');

    postForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const platform = document.getElementById('post-platform').value;
        const message = document.getElementById('post-message').value;
        const scheduleTime = document.getElementById('schedule-time').value;

        const response = await fetch('/api/post_update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ platform, message, schedule_time: scheduleTime }),
        });

        const result = await response.json();

        if (result.success) {
            postResult.textContent = scheduleTime ? 'Post scheduled successfully' : 'Post published successfully';
            postForm.reset();
        } else {
            postResult.textContent = 'Error posting update';
        }
    });
});
