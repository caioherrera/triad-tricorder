import { Component, OnInit } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators'
import { TitleCasePipe, CommonModule } from '@angular/common';

@Component({
  selector: 'menu-breadcrumb',
  imports: [MatCardModule, TitleCasePipe, CommonModule],
  templateUrl: './menu-breadcrumb.html',
  styleUrl: './menu-breadcrumb.scss'
})
export class MenuBreadCrumbComponent implements OnInit { 
    currentRoute: string = "";
    isHome: boolean = true;
    routeParts: string[] = [];

    constructor(private router: Router, private activatedRoute: ActivatedRoute) { }

    ngOnInit() {
        this.router.events.pipe(
            filter(event => event instanceof NavigationEnd)
        ).subscribe(() => {
            this.currentRoute = this.router.url;
            this.isHome = this.currentRoute == '/home';
            this.routeParts = this.currentRoute.split('/').filter(part => part.length > 0).map(part => isNaN(Number(part)) ? part : "#" + part);
        });
    }
}
