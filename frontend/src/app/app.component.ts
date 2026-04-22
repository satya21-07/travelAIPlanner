import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { Component, OnInit, inject } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';

import { DestinationGalleryComponent } from './components/destination-gallery/destination-gallery.component';
import { HistoryStripComponent } from './components/history-strip/history-strip.component';
import { ItineraryResultComponent } from './components/itinerary-result/itinerary-result.component';
import { PlannerFormComponent } from './components/planner-form/planner-form.component';
import { TravelStateService } from './services/travel-state.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    HttpClientModule,
    ReactiveFormsModule,
    PlannerFormComponent,
    ItineraryResultComponent,
    DestinationGalleryComponent,
    HistoryStripComponent,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent implements OnInit {
  protected readonly state = inject(TravelStateService);

  ngOnInit(): void {
    this.state.init();
  }
}
