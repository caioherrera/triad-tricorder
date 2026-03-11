import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { environment } from '../environments/environment';

const base_url = environment.backendBaseUrl;
const applications_api: string = base_url + '/api/applications';
const single_application_api: string = applications_api +  '/<application_id>';
const save_application_api: string = applications_api + '/upsert';

export class Application {

    id: number | null = null;
    application_name: string | null = null;
    command_line: string | null = null;
}

@Injectable({providedIn: "root"})
export class ApplicationService {
    
    constructor(private http: HttpClient) { }

    getApplications(): Observable<Application[]> {

        return this.http.get<Application[]>(applications_api);
    }

    getApplication(id: number): Observable<Application> {

        let url: string = single_application_api.replace("<application_id>", id.toString());

        return this.http.get<Application>(url);
    }

    upsertApplication(app: Application): Observable<Application> {
        let url: string = save_application_api;
        return this.http.post<Application>(url, app);   
    }

}