import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { SessionWorkload } from "./session-service";
import { environment } from '../environments/environment';

const base_url = environment.backendBaseUrl;

const session_profiles_api: string = base_url + '/api/sessions/<session_id>/profiles';

export class Profile {
    id: number | null = null;
    session_workload: SessionWorkload | null = null;
    group: string | null = null;
    cpu_readings: string | null = null;
    ram_readings: string | null = null;
    io_data_readings: string | null = null;
    io_bytes_readings: string | null = null;
    file_path: string | null = null;

    cpu_readings_array: number[] = [];
    ram_readings_array: number[] = [];
    io_data_readings_array: number[] = [];
    io_bytes_readings_array: number[] = [];
}

@Injectable({providedIn: "root"})
export class ProfileService {
    
    constructor(private http: HttpClient) { }

    getProfiles(session_id: number): Observable<Profile[]> {
        let url: string = session_profiles_api.replace("<session_id>", session_id.toString());
        return this.http.get<Profile[]>(url);
    }

    loadProfileReadings(profile: Profile) {
        profile.cpu_readings_array = profile.cpu_readings?.split(" ").map(x => Number(Number(x).toFixed(2))) || [];
        profile.ram_readings_array = profile.ram_readings?.split(" ").map(x => Number(Number(x).toFixed(2))) || [];
        profile.io_data_readings_array = profile.io_data_readings?.split(" ").map(x => Number(Number(x).toFixed(2))) || [];
        profile.io_bytes_readings_array = profile.io_bytes_readings?.split(" ").map(x => Number(Number(x).toFixed(2))) || [];
    }
}