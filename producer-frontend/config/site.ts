export type SiteConfig = typeof siteConfig;

export const siteConfig = {
  name: "Smartland Producer",
  description: "",
  navItems: [
    {
      label: "Home",
      href: "/home",
    },
  ],
  navMenuItems: [
    {
      label: "Profile",
      href: "/profile",
    },
    {
      label: "Dashboard",
      href: "/dashboard",
    },
    {
      label: "Logout",
      href: "/logout",
    },
  ],
  links: {
    login: "/api/auth/login",
  },
};
