module.exports = {
    apps: [
        {
            name: 'backend',
            script: 'src/api/chat_api.py',
            interpreter: 'python',
            env: {
                PYTHONPATH: '.'
            }
        },
        {
            name: 'frontend',
            cwd: './frontend',
            script: 'npm',
            args: 'start', // or 'run dev' for development
            env: {
                NODE_ENV: 'production'
            }
        },
        {
            name: 'brain',
            script: 'agents/brain_agent.py',
            interpreter: 'python',
            env: {
                PYTHONPATH: '.'
            }
        },
        {
            name: 'watchers',
            script: 'watchers.py',
            interpreter: 'python',
            env: {
                PYTHONPATH: '.'
            }
        }
    ]
};
