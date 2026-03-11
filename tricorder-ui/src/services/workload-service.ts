import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { Application } from "./application-service";
import { environment } from '../environments/environment';

const base_url = environment.backendBaseUrl;

const applications_api: string = base_url + '/api/applications';
const sessions_api: string = base_url + '/api/sessions';
const workloads_api: string = base_url + '/api/workloads';

const single_workload_api: string = workloads_api + '/<workload_id>';
const application_workloads_api: string = applications_api + '/<application_id>/workloads';
const workloads_from_session_api: string = sessions_api + '/<session_id>/workloads';

const save_workload_api: string = workloads_api + '/upsert';

export class Workload {

    id: number | null = null;
    workload_name: string | null = null;
    workload_desc: string | null = null;
    application: Application | null = null;
    input_value: string | null = null;
}

@Injectable({providedIn: "root"})
export class WorkloadService {
    
    constructor(private http: HttpClient) { }
    
    getWorkload(id: number): Observable<Workload> {

        let url: string = single_workload_api.replace("<workload_id>", id.toString());
        return this.http.get<Workload>(url);
    }

    getWorkloads(): Observable<Workload[]> {

        let url: string = workloads_api;
        return this.http.get<Workload[]>(url);
    }

    getApplicationWorkloads(id: number): Observable<Workload[]> {
        
        let url: string = application_workloads_api.replace("<application_id>", id.toString());
        return this.http.get<Workload[]>(url);
    }

    getWorkloadsFromSession(id: number): Observable<Workload[]> {

        let url: string = workloads_from_session_api.replace("<session_id>", id.toString());
        return this.http.get<Workload[]>(url);
    }	

    upsertWorkload(workload: Workload): Observable<Workload> {

        let url: string = save_workload_api;
        return this.http.post<Workload>(url, workload);   
    }
}