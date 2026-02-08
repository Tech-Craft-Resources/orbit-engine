import { Link as RouterLink } from "@tanstack/react-router";
import { ChevronsUpDown, LogOut, Settings } from "lucide-react";

import { Appearance } from "@/components/Common/Appearance";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import useAuth from "@/hooks/useAuth";
import { getInitials } from "@/utils";

const navLinks = [
  { href: "#features", label: "Features" },
  { href: "#benefits", label: "Benefits" },
  { href: "#stats", label: "Results" },
];

export function LandingNav() {
  const { user, logout } = useAuth();

  const fullName = user ? `${user.first_name} ${user.last_name}` : "";

  return (
    <header className="sticky top-0 z-50 border-b bg-background/80 backdrop-blur-sm">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
        <RouterLink to="/" className="flex items-center gap-2">
          <img
            src="/assets/images/orbit-engine-logo.png"
            alt="OrbitEngine"
            className="h-8 dark:hidden"
          />
          <img
            src="/assets/images/orbit-engine-logo-dark.png"
            alt="OrbitEngine"
            className="h-8 hidden dark:block"
          />
          <span className="text-xl">
            <span className="font-bold">Orbit</span>Engine
          </span>
        </RouterLink>
        <nav className="hidden items-center gap-6 md:flex">
          {navLinks.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="text-sm text-muted-foreground transition-colors hover:text-foreground"
            >
              {link.label}
            </a>
          ))}
        </nav>
        <div className="flex items-center gap-3">
          <Appearance />
          {user ? (
            <>
              <Button size="sm" asChild>
                <RouterLink to="/dashboard">Go to Dashboard</RouterLink>
              </Button>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="sm" className="gap-2">
                    <Avatar className="size-6">
                      <AvatarFallback className="bg-zinc-600 text-white text-xs">
                        {getInitials(fullName || "User")}
                      </AvatarFallback>
                    </Avatar>
                    <ChevronsUpDown className="size-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-56">
                  <DropdownMenuLabel>
                    <div className="flex flex-col space-y-1">
                      <p className="text-sm font-medium">{fullName}</p>
                      <p className="text-xs text-muted-foreground">
                        {user.email}
                      </p>
                    </div>
                  </DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <RouterLink to="/dashboard/settings">
                    <DropdownMenuItem>
                      <Settings />
                      User Settings
                    </DropdownMenuItem>
                  </RouterLink>
                  <DropdownMenuItem onClick={logout}>
                    <LogOut />
                    Log Out
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </>
          ) : (
            <>
              <Button variant="ghost" size="sm" asChild>
                <RouterLink to="/login">Log In</RouterLink>
              </Button>
              <Button size="sm" asChild>
                <RouterLink to="/signup">Get Started</RouterLink>
              </Button>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
