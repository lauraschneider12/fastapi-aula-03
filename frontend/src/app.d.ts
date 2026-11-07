// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces

declare global {
    interface Window {
        google: {
            charts: {
                load: (
                    version: string,
                    options: { packages: string[] }
                ) => void;
                setOnLoadCallback: (callback: () => void) => void;
            };
            visualization: {
                arrayToDataTable: (
                    data: (string | number)[][]
                ) => any;
                BarChart: new (element: HTMLElement) => {
                    draw: (data: any, options: any) => void;
                };
            };
        };
    }

    namespace App {
        // interface Error {}
        // interface Locals {}
        // interface PageData {}
        // interface PageState {}
        // interface Platform {}
    }
}

export {};