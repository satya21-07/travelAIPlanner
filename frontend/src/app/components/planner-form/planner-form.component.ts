import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { animate, style, transition, trigger } from '@angular/animations';
import { Destination } from '../../travel.types';
import { DESTINATION_SEARCH_OPTIONS, DestinationSearchOption } from '../../destination-search.data';

@Component({
  selector: 'app-planner-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './planner-form.component.html',
  styleUrl: './planner-form.component.css',
  animations: [
    trigger('panelIn', [
      transition(':enter', [
        style({ opacity: 0, transform: 'translateY(22px)' }),
        animate('520ms cubic-bezier(.2,.8,.2,1)', style({ opacity: 1, transform: 'translateY(0)' })),
      ]),
    ]),
  ],
})
export class PlannerFormComponent {
  @Input({ required: true }) form!: FormGroup;
  @Input() destinations: Destination[] = [];
  @Input() loading = false;
  @Input() error = '';
  @Output() submitPlan = new EventEmitter<void>();
  showDestinationSuggestions = false;
  showStartLocationSuggestions = false;

  get destinationControl(): FormControl<string | null> {
    return this.form.get('destination') as FormControl<string | null>;
  }

  get startLocationControl(): FormControl<string | null> {
    return this.form.get('start_location') as FormControl<string | null>;
  }

  get filteredDestinationSuggestions(): DestinationSearchOption[] {
    return this.filterSuggestions(this.destinationControl.value || '');
  }

  get filteredStartLocationSuggestions(): DestinationSearchOption[] {
    return this.filterSuggestions(this.startLocationControl.value || '');
  }

  openDestinationSuggestions(): void {
    this.showDestinationSuggestions = true;
  }

  closeDestinationSuggestions(): void {
    setTimeout(() => {
      this.showDestinationSuggestions = false;
    }, 120);
  }

  openStartLocationSuggestions(): void {
    this.showStartLocationSuggestions = true;
  }

  closeStartLocationSuggestions(): void {
    setTimeout(() => {
      this.showStartLocationSuggestions = false;
    }, 120);
  }

  selectDestination(destination: DestinationSearchOption): void {
    this.destinationControl.setValue(destination.name);
    this.destinationControl.markAsDirty();
    this.destinationControl.markAsTouched();
    this.showDestinationSuggestions = false;
  }

  selectStartLocation(destination: DestinationSearchOption): void {
    this.startLocationControl.setValue(destination.name);
    this.startLocationControl.markAsDirty();
    this.startLocationControl.markAsTouched();
    this.showStartLocationSuggestions = false;
  }

  private filterSuggestions(queryValue: string): DestinationSearchOption[] {
    const query = queryValue.trim().toLowerCase();
    const apiOptions = this.destinations.map((destination) => ({
      name: destination.name,
      region: (destination as Destination & { region?: string }).region || 'India',
    }));
    const options = this.mergeDestinationOptions([...DESTINATION_SEARCH_OPTIONS, ...apiOptions]);

    if (!query) {
      return options.slice(0, 10);
    }

    return options
      .filter((option) =>
        option.name.toLowerCase().startsWith(query) ||
        option.region.toLowerCase().startsWith(query)
      )
      .slice(0, 12);
  }

  private mergeDestinationOptions(options: DestinationSearchOption[]): DestinationSearchOption[] {
    const seen = new Set<string>();
    const merged: DestinationSearchOption[] = [];

    for (const option of options) {
      const key = `${option.name.trim().toLowerCase()}|${option.region.trim().toLowerCase()}`;
      if (seen.has(key)) {
        continue;
      }
      seen.add(key);
      merged.push(option);
    }

    return merged.sort((a, b) => {
      const nameCompare = a.name.localeCompare(b.name);
      return nameCompare !== 0 ? nameCompare : a.region.localeCompare(b.region);
    });
  }
}
