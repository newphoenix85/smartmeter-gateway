/** @type {import('next').NextConfig} */
const nextConfig = {
    env: {
        NEXT_PUBLIC_API_URL: 'https://producer.smartland.lan/api'
    },
    redirects: async () => {
        return [
            {
                source: "/",
                destination: "https://producer.smartland.lan/api/auth/login",
                permanent: true
            }
        ]
    },
}

module.exports = nextConfig
