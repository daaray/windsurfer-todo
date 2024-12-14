import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import { QInput, QBtn } from 'quasar';
import TodoForm from '../components/TodoForm.vue';

describe('TodoForm', () => {
  const mountOptions = {
    global: {
      stubs: {
        QInput,
        QBtn,
      },
    },
  };

  it('renders properly', () => {
    const wrapper = mount(TodoForm, mountOptions);
    expect(wrapper.exists()).toBe(true);
    expect(wrapper.find('form').exists()).toBe(true);
    expect(wrapper.findComponent(QInput).exists()).toBe(true);
  });

  it('emits add-todo event when form is submitted', async () => {
    const wrapper = mount(TodoForm, mountOptions);
    const input = wrapper.findComponent(QInput);

    await input.setValue('New Todo Item');
    await wrapper.find('form').trigger('submit.prevent');

    expect(wrapper.emitted('add-todo')).toBeTruthy();
    expect(wrapper.emitted('add-todo')[0][0]).toBe('New Todo Item');
  });

  it('clears input after form submission', async () => {
    const wrapper = mount(TodoForm, mountOptions);
    const input = wrapper.findComponent(QInput);

    await input.setValue('New Todo Item');
    await wrapper.find('form').trigger('submit.prevent');

    expect(input.vm.modelValue).toBe('');
  });

  it('does not emit event when input is empty', async () => {
    const wrapper = mount(TodoForm, mountOptions);
    await wrapper.find('form').trigger('submit.prevent');
    expect(wrapper.emitted('add-todo')).toBeFalsy();
  });
});
