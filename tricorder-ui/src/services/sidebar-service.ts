import { Injectable } from "@angular/core"

import { Observable, Subject } from "rxjs";

@Injectable({providedIn: "root"})
export class SidebarService {

    private shouldOpenSidebar: Subject<boolean>;
    private currSidebarValue: boolean;

    constructor() {
        this.shouldOpenSidebar = new Subject<boolean>();
        this.currSidebarValue = false;
        this.shouldOpenSidebar.next(this.currSidebarValue);
    }

    toggleSidebar(): void {
        this.currSidebarValue = !this.currSidebarValue;
        this.shouldOpenSidebar.next(this.currSidebarValue);
    }

    onSidebarToggle(): Observable<boolean> {
        return this.shouldOpenSidebar;
    }

}