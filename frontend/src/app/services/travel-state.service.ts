import { Injectable, inject } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { FormBuilder, Validators } from '@angular/forms';
import { BehaviorSubject, finalize } from 'rxjs';
import { TravelApiService } from './travel-api.service';
import { Destination, Itinerary, ItineraryPayload } from '../travel.types';

@Injectable({ providedIn: 'root' })
export class TravelStateService {
  private readonly fb = inject(FormBuilder);
  private readonly api = inject(TravelApiService);

  private readonly loadingSubject = new BehaviorSubject<boolean>(false);
  private readonly errorSubject = new BehaviorSubject<string>('');
  private readonly destinationsSubject = new BehaviorSubject<Destination[]>([]);
  private readonly historySubject = new BehaviorSubject<Itinerary[]>([]);
  private readonly selectedPlanSubject = new BehaviorSubject<Itinerary | null>(null);
  
  loading$ = this.loadingSubject.asObservable();
  error$ = this.errorSubject.asObservable();
  destinations$ = this.destinationsSubject.asObservable();
  history$ = this.historySubject.asObservable();
  selectedPlan$ = this.selectedPlanSubject.asObservable();

  formVisible = true;
  historyVisible = false;

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

  init(): void {
    this.refreshDestinations();
    this.refreshHistory();
  }

  createPlan(): void {
    if (this.form.invalid) return;

    this.loadingSubject.next(true);
    this.errorSubject.next('');
    
    const value = this.form.getRawValue();
    const payload: ItineraryPayload = {
      ...value,
      interests: value.interests.split(',').map(s => s.trim()).filter(Boolean),
    };

    this.api.createItinerary(payload)
      .pipe(finalize(() => this.loadingSubject.next(false)))
      .subscribe({
        next: (plan) => {
          this.selectedPlanSubject.next(plan);
          const currentHistory = this.historySubject.value;
          this.historySubject.next([plan, ...currentHistory.filter(h => h.id !== plan.id)].slice(0, 8));
          this.formVisible = false;
        },
        error: (error: HttpErrorResponse) => this.errorSubject.next(this.formatApiError(error))
      });
  }

  useDestination(dest: Destination): void {
    this.form.patchValue({
      destination: dest.name,
      budget: Math.max(dest.base_daily_cost * 4 * this.form.controls.travelers.value, 12000),
      interests: dest.tags.join(', '),
    });
  }

  selectFromHistory(plan: Itinerary): void {
    this.selectedPlanSubject.next(plan);
    this.formVisible = false;
    this.historyVisible = false;
  }

  private refreshDestinations(): void {
    this.api.getDestinations().subscribe({
      next: (items) => this.destinationsSubject.next(items),
      error: () => this.destinationsSubject.next([])
    });
  }

  private refreshHistory(): void {
    this.api.getItineraries().subscribe({
      next: (items) => this.historySubject.next(items),
      error: () => this.historySubject.next([])
    });
  }

  private formatApiError(error: HttpErrorResponse): string {
    const detail = error.error?.detail;
    if (typeof detail === 'string' && detail.trim()) {
      return detail;
    }

    if (typeof error.error?.message === 'string' && error.error.message.trim()) {
      return error.error.message;
    }

    if (error.status === 0) {
      return 'Could not reach the backend at http://localhost:8000. Make sure the FastAPI server is running.';
    }

    if (typeof error.error === 'string' && error.error.trim()) {
      return error.error;
    }

    return `Could not create the itinerary${error.status ? ` (${error.status})` : ''}.`;
  }
}
