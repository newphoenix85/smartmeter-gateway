/** @type {import('next').NextConfig} */
const nextConfig = {
    env: {
        NEXT_PUBLIC_API_URL: 'https://consumer.tenant.lan:8443/api'
    },
    redirects: async () => {
        return [
            {
                source: "/",
                destination: "https://consumer.tenant.lan:8443/api/auth/login",
                permanent: true
            }
        ]
    },
}

module.exports = nextConfig
