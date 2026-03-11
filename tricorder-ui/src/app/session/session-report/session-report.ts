import { ChangeDetectionStrategy, Component, signal } from '@angular/core';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatGridListModule } from '@angular/material/grid-list';
import { CommonModule, Location } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatListModule } from '@angular/material/list';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatSelectModule } from '@angular/material/select';
import { Session, SessionService, SessionWorkload } from '../../../services/session-service';
import { Profile, ProfileService } from '../../../services/profile-service';
import { ActivatedRoute } from '@angular/router';
import { MatExpansionModule } from '@angular/material/expansion';

@Component({
  selector: 'session-report',
  imports: [ CommonModule, MatInputModule, MatFormFieldModule, FormsModule, MatIconModule, MatGridListModule, MatTableModule,
    MatCheckboxModule, MatAutocompleteModule, ReactiveFormsModule, MatSelectModule, MatListModule, MatExpansionModule ],
  templateUrl: './session-report.html',
  styleUrls: ['../../../styles.scss', './session-report.scss']
})
export class SessionReportComponent { 

    session: Session | null = null;
    sessionWorkloads: SessionWorkload[] = [];
    profiles: { [id: number] : Profile[] } = {};

    columnLabels: string[] = ["id", "file_path", "group", "actions"];

    constructor(
        private sessionService: SessionService,
        private profileService: ProfileService,
        private activatedRoute: ActivatedRoute,
        private location: Location
    ) { }
    
    ngOnInit() {

        this.activatedRoute.paramMap.subscribe(params => {
            let idParam: string | null = params.get('id');
            
            if(idParam !== null) {
                let id = Number(idParam);

                this.sessionService.getSessionDetails(id).subscribe(sessionDetails => {
                    
                    this.sessionWorkloads = sessionDetails;

                    if(sessionDetails.length > 0) {
                        if(!this.session)
                            this.session = sessionDetails[0].session;
                    }                    

                    this.sessionWorkloads.forEach(sw => {

                        let monitoring_end = Number(sw.monitoring_end_time_seconds);
                        let monitoring_start = Number(sw.monitoring_start_time_seconds);
                        let monitoring_elapsed_time = (!isNaN(monitoring_end) && !isNaN(monitoring_start)) ? monitoring_end - monitoring_start : -1;

                        let analysis_end = Number(sw.analysis_end_time_seconds);
                        let analysis_start = Number(sw.analysis_start_time_seconds);
                        let analysis_elapsed_time = (!isNaN(analysis_end) && !isNaN(analysis_start)) ? analysis_end - analysis_start : -1;

                        if (monitoring_elapsed_time >= 60) {
                            sw.monitoring_elapsed_time = parseInt((monitoring_elapsed_time / 60).toString(), 10).toString() + " minutes";
                            if (monitoring_elapsed_time % 60 !== 0) {
                                sw.monitoring_elapsed_time += " and " + (monitoring_elapsed_time % 60).toFixed(2) + " seconds";
                            }
                        }
                        else if (monitoring_elapsed_time >= 0) {
                            sw.monitoring_elapsed_time = monitoring_elapsed_time.toFixed(2) + " seconds";
                        }
                        else {
                            sw.monitoring_elapsed_time = "N/A";
                        }

                        if (analysis_elapsed_time >= 60) {
                            sw.analysis_elapsed_time = parseInt((analysis_elapsed_time / 60).toString(), 10).toString() + " minutes";
                            if (analysis_elapsed_time % 60 !== 0) {
                                sw.analysis_elapsed_time += " and " + (analysis_elapsed_time % 60).toFixed(2) + " seconds";
                            }
                        }
                        else if (analysis_elapsed_time >= 0) {
                            sw.analysis_elapsed_time = analysis_elapsed_time.toFixed(2) + " seconds";
                        }
                        else {
                            sw.analysis_elapsed_time = "N/A";
                        }

                        sw.text_verdict = (sw.verdict === 1) ? "Anomaly Detected after " + (sw.iterations_to_detect || 0) + " out of " + ((sw.total_iterations || 0) + 1) + " iterations" : (sw.verdict === 0) ? "No Anomaly Detected" : "N/A";
                    });
                });

                this.profileService.getProfiles(id).subscribe(profiles => {

                    profiles.forEach(profile => {
                        this.profileService.loadProfileReadings(profile);
                        let key = profile.session_workload?.id as number;
                        this.profiles[key] = (this.profiles[key] || []).concat(profile);
                    });
                    
                });                
            }
        });
    }

    back() {
        this.location.back();
    }
}
