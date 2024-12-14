import js from '@eslint/js';
import vueParser from 'vue-eslint-parser';
import vuePlugin from 'eslint-plugin-vue';
import prettier from 'eslint-config-prettier';

export default [
  {
    ignores: ['dist/*', 'coverage/*'],
  },
  js.configs.recommended,
  {
    files: ['**/*.vue', '**/*.js', '**/*.cjs', '**/*.mjs'],
    languageOptions: {
      parser: vueParser,
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        console: 'readonly',
        window: 'readonly',
        process: 'readonly',
      },
    },
    plugins: {
      vue: vuePlugin,
    },
    rules: {
      ...vuePlugin.configs.base.rules,
      ...vuePlugin.configs['vue3-recommended'].rules,
      'vue/multi-word-component-names': 'off',
      'vue/attributes-order': [
        'error',
        {
          order: [
            'DEFINITION',
            'LIST_RENDERING',
            'CONDITIONALS',
            'RENDER_MODIFIERS',
            'GLOBAL',
            'UNIQUE',
            'TWO_WAY_BINDING',
            'OTHER_DIRECTIVES',
            'OTHER_ATTR',
            'EVENTS',
            'CONTENT',
          ],
        },
      ],
      'vue/comment-directive': 'off',
      'no-console': 'off',
      'no-debugger': 'off',
    },
  },
  prettier,
];
