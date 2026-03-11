import { defineConfig } from 'vite';
import angular from '@angular-devkit/build-angular/plugins/vite';

export default defineConfig({
    plugins: [angular()],
    server: {
        host: '0.0.0.0',
        port: 7072,
        allowedHosts: [
            'andromeda.lasdpc.icmc.usp.br',
            'localhost', 
            '127.0.0.1'
        ]
    }
});