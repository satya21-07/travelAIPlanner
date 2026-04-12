import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { Component, OnInit, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

import { DestinationGalleryComponent } from './destination-gallery.component';
import { HistoryStripComponent } from './history-strip.component';
import { ItineraryResultComponent } from './itinerary-result.component';
import { PlannerFormComponent } from './planner-form.component';
import { TravelApiService } from './travel-api.service';
import { Destination, Itinerary, ItineraryPayload } from './travel.types';

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
  private readonly fb = inject(FormBuilder);
  private readonly api = inject(TravelApiService);

  loading = false;
  error = '';
  destinations: Destination[] = [];
  history: Itinerary[] = [];
  selectedPlan: Itinerary | null = null;

  form = this.fb.nonNullable.group({
    destination: ['Goa', [Validators.required, Validators.minLength(2)]],
    start_location: [''],
    days: [4, [Validators.required, Validators.min(1), Validators.max(21)]],
    travelers: [2, [Validators.required, Validators.min(1), Validators.max(12)]],
    budget: [25000, [Validators.required, Validators.min(1)]],
    currency: ['INR', [Validators.required]],
    travel_style: ['balanced', [Validators.required]],
    interests: ['beach, food, markets'],
  });

  ngOnInit(): void {
    this.loadDestinations();
    this.loadHistory();
  }

  createPlan(): void {
    if (this.form.invalid) {
      return;
    }

    this.loading = true;
    this.error = '';
    const value = this.form.getRawValue();
    const payload: ItineraryPayload = {
      ...value,
      interests: value.interests.split(',').map((item) => item.trim()).filter(Boolean),
    };

    this.api.createItinerary(payload).subscribe({
      next: (plan) => {
        this.selectedPlan = plan;
        this.history = [plan, ...this.history.filter((item) => item.id !== plan.id)].slice(0, 8);
        this.loading = false;
      },
      error: () => {
        this.error = 'Could not create the itinerary. Make sure the backend is running on port 8000.';
        this.loading = false;
      },
    });
  }

  useDestination(destination: Destination): void {
    this.form.patchValue({
      destination: destination.name,
      budget: Math.max(destination.base_daily_cost * 4 * this.form.controls.travelers.value, 12000),
      interests: destination.tags.join(', '),
    });
  }

  private loadDestinations(): void {
    this.api.getDestinations().subscribe({
      next: (items) => (this.destinations = items),
      error: () => (this.destinations = []),
    });
  }

  private loadHistory(): void {
    this.api.getItineraries().subscribe({
      next: (items) => (this.history = items),
      error: () => (this.history = []),
    });
  }
}

