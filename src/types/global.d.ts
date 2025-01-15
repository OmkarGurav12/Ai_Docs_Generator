/// <reference types="react" />

declare module "@radix-ui/react-select" {
  export * from "@radix-ui/react-select";
}

declare module "lucide-react" {
  export * from "lucide-react";
}

declare global {
  namespace JSX {
    interface IntrinsicElements extends React.JSX.IntrinsicElements {}
  }
}